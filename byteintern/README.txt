SENYAO · 产品、视觉与动态创作专题
2026-11-01

入口：index.html
线上路径：https://senyaolu-lab.github.io/byteintern/

八个案例
01 GrowthPilot：广告策略交互原型、4 个合成业务情景、预算约束、实验样本估算。
02 FlowDesk：Agent 任务工作台交互原型、失败重试、人工确认、引用与运行记录。
03 CITY REMIX：3 种图文创意模式、可编辑图片与文案、动画预览、SVG/配置导出。
04 PAPER CITY：创作者挑战、3 条参与路径、7 天内容排期、投稿自检与事件设计。
05 SYNC / 同频：品牌主视觉、24 秒 1080P 产品动效、6 页可编辑 PPTX、分镜与字幕。
06 留一盏灯：30 秒 1080P 公共沟通动态图形影片、原创合成音轨、分镜与字幕。
07 LANTERN COURIER：角色设定、场景关键帧、4 种光照对照、资产规范与人工验收。
08 RAIN MARKET：摄影/水粉/手作微缩三种表达、失败版本、对比界面与人工标注表。

使用方式
建议先进入 byteintern-portfolio 文件夹，再以静态服务器打开，确保本地存储、下载和媒体功能稳定：
python -m http.server 8766
打开 http://127.0.0.1:8766/
也可直接打开 index.html；不同浏览器对 file:// 页面的存储限制可能不同。

可编辑材料
网页原型：cases/ 下的 HTML、CSS、JavaScript。
图像原图：assets/ 下 PNG；evidence/image-prompts.json 为提示词与参考关系。
视频：cases/motion/ 下 MP4；SRT/VTT 为字幕；evidence/motion/render-films.py 为制作脚本。
提案：cases/motion/sync-pitch.pptx。标题、正文、流程与表格可编辑，位图视觉保留为图片。
运营与产品：evidence/ 下 PRD、SOP、JSON 数据、模板和实际检查报告。

测试复现（同样从 byteintern-portfolio 文件夹运行）
node evidence/product/evaluate.cjs
node evidence/creator/creator-rules.test.cjs
node evidence/art/verify-art.cjs
请以对应目录里的实际测试报告说明为准。

项目性质
这组作品为独立概念项目，由 AI 辅助构思、制作与实现，不是字节跳动或旗下产品的真实商业委托。
所有业务数据和研究场景均为合成或假设；未开展真实投放、访谈或线上 A/B 实验。
产品原型使用确定性规则，不接入真实模型或商家账户。CITY REMIX 是浏览器创意原型。
影片为程序化动态图形，不是 Seedance 等视频模型的实测输出；角色是二维概念美术，不含三维网格、绑定或动画资产。
图片保留人工检查与失败迭代，不能把跨图一致性或风格转换当成模型性能基准。
岗位路径帮助选择阅读顺序，不构成招聘方的认可或审核结论。
