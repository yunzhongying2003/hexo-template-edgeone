/**
 * Hexo Generator: 文章关系图谱
 * 在 hexo generate 时自动生成 graph.json
 * 
 * 关联逻辑：
 *   - 标签匹配（权重 1）
 *   - 分类匹配（权重 3）
 *   - 正文关键词重叠（权重 0.5）
 * 
 * 即使标签/分类无匹配，正文关键词重叠也能建立关联。
 */

const fs = require('fs');
const path = require('path');
const segmentit = require('segmentit');

hexo.extend.generator.register('graph', function(locals) {
    console.log('[Graph Generator] Running...');
    const postsDir = path.join(this.source_dir, '_posts');
    const outputDir = path.join(this.public_dir, 'graph');
    
    if (!fs.existsSync(postsDir)) return;
    
    // ============ Parse all posts ============
    const posts = [];
    const files = fs.readdirSync(postsDir).filter(f => f.endsWith('.md'));
    
    for (const file of files) {
        const content = fs.readFileSync(path.join(postsDir, file), 'utf-8');
        const match = content.match(/^---\n([\s\S]*?)\n---/);
        if (!match) continue;
        
        const fm = {};
        match[1].split('\n').forEach(line => {
            const idx = line.indexOf(':');
            if (idx === -1) return;
            const key = line.substring(0, idx).trim();
            let val = line.substring(idx + 1).trim();
            if (val.startsWith('[') && val.endsWith(']')) {
                val = val.slice(1, -1).split(',').map(s => s.trim().replace(/^["']|["']$/g, ''));
            } else {
                val = val.replace(/^["']|["']$/g, '');
            }
            fm[key] = val;
        });
        
        if (!fm.title) return;
        
        const slug = file.replace('.md', '');
        const tags = Array.isArray(fm.tags) ? fm.tags : [];
        const categories = Array.isArray(fm.categories) ? fm.categories : (fm.categories ? [fm.categories] : []);
        
        // Extract body content (everything after frontmatter)
        const bodyMatch = content.match(/^---\n[\s\S]*?\n---\n([\s\S]*)$/);
        const body = bodyMatch ? bodyMatch[1] : '';
        
        // Extract keywords from body
        const keywords = extractKeywords(body);
        
        posts.push({ slug, title: fm.title, date: fm.date || '', tags, categories, keywords });
    }
    
    // ============ Compute edges ============
    const TAG_WEIGHT = 1;
    const CATEGORY_WEIGHT = 3;
    const KEYWORD_WEIGHT = 0.5;
    const edges = [];
    
    for (let i = 0; i < posts.length; i++) {
        for (let j = i + 1; j < posts.length; j++) {
            const p1 = posts[i], p2 = posts[j];
            
            const sharedTags = p1.tags.filter(t => p2.tags.includes(t));
            const sharedCats = p1.categories.filter(c => p2.categories.includes(c));
            
            // Keyword overlap
            const sharedKeywords = p1.keywords.filter(k => p2.keywords.includes(k));
            
            // Keyword contribution rules:
            // - If already have tag/category match: always count keywords
            // - If only keyword match (no tag/cat): require ≥ 2 keywords to avoid noise
            const hasTagCat = sharedTags.length > 0 || sharedCats.length > 0;
            const kwContrib = (hasTagCat || sharedKeywords.length >= 2)
                ? sharedKeywords.length * KEYWORD_WEIGHT
                : 0;
            
            const weight = 
                sharedTags.length * TAG_WEIGHT + 
                sharedCats.length * CATEGORY_WEIGHT + 
                kwContrib;
            
            if (weight > 0) {
                edges.push({
                    from: p1.slug,
                    to: p2.slug,
                    weight,
                    shared_tags: sharedTags,
                    shared_categories: sharedCats,
                    shared_keywords: sharedKeywords
                });
            }
        }
    }
    
    edges.sort((a, b) => b.weight - a.weight);
    
    // ============ Build nodes ============
    const nodes = posts.map(p => ({
        id: p.slug,
        label: p.title,
        title: p.title,
        date: p.date,
        tags: p.tags,
        categories: p.categories,
        size: Math.max(10, Math.min(40, 10 + p.tags.length * 3 + p.categories.length * 5))
    }));
    
    // ============ Output ============
    fs.mkdirSync(outputDir, { recursive: true });
    const output = {
        nodes,
        edges,
        meta: {
            total_posts: posts.length,
            total_edges: edges.length,
            tag_weight: TAG_WEIGHT,
            category_weight: CATEGORY_WEIGHT,
            keyword_weight: KEYWORD_WEIGHT
        }
    };
    
    fs.writeFileSync(path.join(outputDir, 'graph.json'), JSON.stringify(output, null, 2));
    console.log('[Graph Generator] ' + nodes.length + ' nodes, ' + edges.length + ' edges');
});

/**
 * Extract top keywords from article body using segmentit
 * Strips markdown formatting, segments text, filters stop words
 */
function extractKeywords(body) {
    if (!body || body.length < 50) return [];
    
    // Strip markdown formatting
    const plain = body
        .replace(/```[\s\S]*?```/g, '')        // code blocks
        .replace(/`[^`]*`/g, '')               // inline code
        .replace(/!\[([^\]]*)\]\([^)]+\)/g, '$1')  // images -> alt text
        .replace(/\[([^\]]*)\]\([^)]+\)/g, '$1')  // links -> text
        .replace(/#{1,6}\s*/g, '')             // headers
        .replace(/[-*_]{3,}/g, '')             // horizontal rules
        .replace(/[*_~]/g, '')                 // bold/italic markers
        .replace(/</g, ' ')                    // HTML tags (simplified)
        .replace(/\n+/g, ' ')                  // newlines -> spaces
        .trim();
    
    // Segment text using segmentit
    const seg = new segmentit.Segment();
    segmentit.useDefault(seg);
    const words = seg.doSegment(plain);
    
    // Common Chinese stop words
    const stopWords = new Set([
        '的', '了', '是', '在', '我', '有', '和', '就', '不', '人', '都', '一', '一个',
        '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好',
        '自己', '这', '他', '她', '它', '们', '那', '些', '什么', '这个', '那个', '这样',
        '那样', '可以', '能', '但', '但是', '而', '而且', '因为', '所以', '如果', '虽然',
        '还是', '或者', '并且', '与', '或', '及', '等', '之', '其', '所', '以', '为',
        '被', '把', '让', '给', '从', '向', '对', '关于', '通过', '根据', '按照', '由于',
        '因此', '然而', '不过', '尽管', '即使', '无论', '只要', '只有', '除非', '不但',
        '不仅', '不只', '既', '又', '且', '则', '即', '乃', '系', '属', '系', '属于',
        '包括', '包含', '以及', '以及', '等等', '之类', '方面', '问题', '问题', '方法',
        '方式', '步骤', '过程', '时候', '时间', '地方', '部分', '情况', '内容', '功能',
        '使用', '需要', '应该', '可能', '已经', '开始', '结束', '完成', '进行', '实现',
        '支持', '提供', '设置', '配置', '安装', '运行', '打开', '点击', '选择', '输入',
        '输出', '显示', '查看', '找到', '知道', '理解', '明白', '认为', '觉得', '希望',
        '必须', '一定', '肯定', '确实', '当然', '当然', '其实', '实际', '当然', '当然',
        '另外', '此外', '同时', '另外', '还有', '还有', '最后', '首先', '其次', '再次',
        '总之', '总之', '综上所述', '总之', '总之', '总之', '总之'
    ]);
    
    // Count word frequencies, filter stop words and short words
    const freq = {};
    for (const w of words) {
        const word = w.w;
        if (!word || word.length < 2) continue;
        if (stopWords.has(word)) continue;
        // Skip pure numbers and English-only short words
        if (/^\d+$/.test(word)) continue;
        if (/^[a-zA-Z]+$/.test(word) && word.length < 3) continue;
        freq[word] = (freq[word] || 0) + 1;
    }
    
    // Sort by frequency, return top 20
    return Object.entries(freq)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 20)
        .map(([word]) => word);
}