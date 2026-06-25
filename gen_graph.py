#!/usr/bin/env python3
"""
扫描 Hexo 博客文章，基于标签计算文章间关联度，输出 graph.json
用法: python3 scripts/gen_graph.py
输出: public/graph/graph.json
"""

import os, re, json, glob
from collections import defaultdict

POSTS_DIR = os.path.join(os.path.dirname(__file__), "..", "source", "_posts")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "public", "graph")

# 标签权重：共享标签越多，关联度越高
# 分类权重更高（因为分类更精准）
TAG_WEIGHT = 1
CATEGORY_WEIGHT = 3

def parse_frontmatter(filepath):
    """解析 Markdown 的 YAML frontmatter"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 提取 --- 之间的内容
    match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not match:
        return None
    
    fm = {}
    for line in match.group(1).split("\n"):
        line = line.strip()
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip()
        
        # 解析数组 [a, b, c]
        if val.startswith("[") and val.endswith("]"):
            items = [i.strip().strip('"').strip("'") for i in val[1:-1].split(",")]
            fm[key] = items
        else:
            fm[key] = val.strip('"').strip("'")
    
    return fm

def extract_post_slug(filepath):
    """从文件路径提取文章 slug"""
    filename = os.path.basename(filepath)
    return filename.replace(".md", "")

def main():
    posts_dir = os.path.normpath(POSTS_DIR)
    posts = []
    
    for filepath in sorted(glob.glob(os.path.join(posts_dir, "*.md"))):
        fm = parse_frontmatter(filepath)
        if not fm or "title" not in fm:
            continue
        
        slug = extract_post_slug(filepath)
        tags = fm.get("tags", [])
        categories = fm.get("categories", [])
        if isinstance(categories, str):
            categories = [categories]
        
        posts.append({
            "id": slug,
            "title": fm["title"],
            "date": fm.get("date", ""),
            "tags": tags,
            "categories": categories,
        })
    
    print(f"📚 扫描到 {len(posts)} 篇文章")
    
    # 构建标签索引
    tag_to_posts = defaultdict(set)
    for p in posts:
        for tag in p["tags"]:
            tag_to_posts[tag].add(p["id"])
        for cat in p["categories"]:
            tag_to_posts[f"cat:{cat}"].add(p["id"])
    
    # 计算文章间关联度
    edges = []
    for i in range(len(posts)):
        for j in range(i + 1, len(posts)):
            p1, p2 = posts[i], posts[j]
            
            # 共享标签
            shared_tags = set(p1["tags"]) & set(p2["tags"])
            shared_cats = set(p1["categories"]) & set(p2["categories"])
            
            weight = len(shared_tags) * TAG_WEIGHT + len(shared_cats) * CATEGORY_WEIGHT
            
            if weight > 0:
                edges.append({
                    "from": p1["id"],
                    "to": p2["id"],
                    "weight": weight,
                    "shared_tags": list(shared_tags),
                    "shared_categories": list(shared_cats),
                })
    
    # 按权重排序
    edges.sort(key=lambda e: e["weight"], reverse=True)
    
    # 计算每篇文章的标签数（用于节点大小）
    nodes = []
    for p in posts:
        node_size = max(10, min(40, 10 + len(p["tags"]) * 3 + len(p["categories"]) * 5))
        nodes.append({
            "id": p["id"],
            "label": p["title"],
            "title": p["title"],
            "date": p["date"],
            "tags": p["tags"],
            "categories": p["categories"],
            "size": node_size,
        })
    
    # 输出
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output = {
        "nodes": nodes,
        "edges": edges,
        "meta": {
            "total_posts": len(posts),
            "total_edges": len(edges),
            "tag_weight": TAG_WEIGHT,
            "category_weight": CATEGORY_WEIGHT,
        }
    }
    
    output_path = os.path.join(OUTPUT_DIR, "graph.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 输出: {output_path}")
    print(f"   节点: {len(nodes)}, 边: {len(edges)}")
    print(f"\n📊 关联度 Top 5:")
    for e in edges[:5]:
        n1 = next((n for n in nodes if n["id"] == e["from"]), {})
        n2 = next((n for n in nodes if n["id"] == e["to"]), {})
        print(f"   [{e['weight']}] {n1.get('title','?')[:20]} ↔ {n2.get('title','?')[:20]}")
        if e["shared_tags"]:
            print(f"        标签: {', '.join(e['shared_tags'])}")
        if e["shared_categories"]:
            print(f"        分类: {', '.join(e['shared_categories'])}")

if __name__ == "__main__":
    main()