/**
 * Hexo Generator: 文章关系图谱
 * 在 hexo generate 时自动生成 graph.json
 */

const fs = require('fs');
const path = require('path');

hexo.extend.generator.register('graph', function(locals) {
    console.log('[Graph Generator] Running...');
    const postsDir = path.join(this.source_dir, '_posts');
    const outputDir = path.join(this.public_dir, 'graph');
    
    if (!fs.existsSync(postsDir)) return;
    
    // Parse all posts
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
        
        posts.push({ slug, title: fm.title, date: fm.date || '', tags, categories });
    }
    
    // Build tag index
    const tagToPosts = {};
    for (const p of posts) {
        for (const tag of p.tags) {
            if (!tagToPosts[tag]) tagToPosts[tag] = new Set();
            tagToPosts[tag].add(p.slug);
        }
        for (const cat of p.categories) {
            const key = 'cat:' + cat;
            if (!tagToPosts[key]) tagToPosts[key] = new Set();
            tagToPosts[key].add(p.slug);
        }
    }
    
    // Compute edges
    const TAG_WEIGHT = 1;
    const CATEGORY_WEIGHT = 3;
    const edges = [];
    
    for (let i = 0; i < posts.length; i++) {
        for (let j = i + 1; j < posts.length; j++) {
            const p1 = posts[i], p2 = posts[j];
            const sharedTags = p1.tags.filter(t => p2.tags.includes(t));
            const sharedCats = p1.categories.filter(c => p2.categories.includes(c));
            const weight = sharedTags.length * TAG_WEIGHT + sharedCats.length * CATEGORY_WEIGHT;
            
            if (weight > 0) {
                edges.push({
                    from: p1.slug,
                    to: p2.slug,
                    weight,
                    shared_tags: sharedTags,
                    shared_categories: sharedCats
                });
            }
        }
    }
    
    edges.sort((a, b) => b.weight - a.weight);
    
    // Build nodes
    const nodes = posts.map(p => ({
        id: p.slug,
        label: p.title,
        title: p.title,
        date: p.date,
        tags: p.tags,
        categories: p.categories,
        size: Math.max(10, Math.min(40, 10 + p.tags.length * 3 + p.categories.length * 5))
    }));
    
    // Output
    fs.mkdirSync(outputDir, { recursive: true });
    const output = {
        nodes,
        edges,
        meta: {
            total_posts: posts.length,
            total_edges: edges.length,
            tag_weight: TAG_WEIGHT,
            category_weight: CATEGORY_WEIGHT
        }
    };
    
    fs.writeFileSync(path.join(outputDir, 'graph.json'), JSON.stringify(output, null, 2));
    console.log('[Graph Generator] ' + nodes.length + ' nodes, ' + edges.length + ' edges');
});