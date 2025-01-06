import streamlit as st
from article import get_article_content
from image import process_images
from report import generate_report

st.set_page_config(layout="wide")

def format_outline(outline):
    """将文章大纲格式化为Markdown"""
    markdown = ""
    for level1, level2_dict in outline.items():
        markdown += f"### {level1}\n\n"
        for level2, level3_list in level2_dict.items():
            markdown += f"#### {level2}\n\n"
            for level3 in level3_list:
                markdown += f"- {level3}\n"
            markdown += "\n"
    return markdown

def format_problems(problems):
    """将问题和解决方案格式化为Markdown有序列表"""
    markdown = ""
    for i, problem in enumerate(problems, 1):
        markdown += f"- **问题描述**: {problem['problem']}\n"
        markdown += f"  - **解决方案/见解**: {problem['solution']}\n\n"
    return markdown

def format_priority_score(priority_score):
    """将优先级评分格式化为Markdown无序列表"""
    markdown = f"- **分数**: {priority_score['score']}\n"
    markdown += f"- **评分原因**: {priority_score['reason']}\n"
    markdown += f"- **相关性**: {priority_score['relevance']}\n"
    return markdown

def main():
    st.title("InfoSnap - 信息快拍")

    url = st.text_input("请输入文章URL链接")
    if url:
        soup = get_article_content(url)
        if soup:
            process_images(soup, url, "downloaded_images")
            modified_html = str(soup)
            print(url)
            report = generate_report(url)
            print(report)

            st.markdown("""
                <style>
                    .report-container {
                        max-width: 1200px;
                        margin: auto;
                    }
                    .report-container h3 {
                        font-size: 1.5em; /* 调整三级标题字体大小 */
                    }
                    .report-container h4 {
                        font-size: 1.25em; /* 调整四级标题字体大小 */
                    }
                </style>
            """, unsafe_allow_html=True)

            st.markdown('<div class="report-container">', unsafe_allow_html=True)

            col1, col2, col3 = st.columns([2, 4, 3])

            with col1:
                st.subheader("文章大纲")
                outline_markdown = format_outline(report["文章大纲"])
                st.markdown(outline_markdown, unsafe_allow_html=True)

            with col2:
                st.subheader("文章原文")
                st.components.v1.html(modified_html, height=600, scrolling=True)

            with col3:
                st.subheader("文章分析报告")
                st.markdown("### 标签")
                tags_markdown = " ".join([f"#{tag}" for tag in report['标签']])
                st.markdown(tags_markdown)
                st.markdown("### 优先级评分")
                priority_score_markdown = format_priority_score(report["优先级评分"])
                st.markdown(priority_score_markdown, unsafe_allow_html=True)
                st.markdown("### 本文解决问题")
                problems_markdown = format_problems(report["本文解决问题"])
                st.markdown(problems_markdown, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.error("无法获取文章内容，请检查URL是否正确。")

if __name__ == "__main__":
    main()