两条原创动态图形案例 / 制作证据

sync.mp4：24秒，1920×1080，24fps，576帧，H.264 + AAC双声道。
light.mp4：30秒，1920×1080，24fps，720帧，H.264 + AAC双声道。

制作方式
Pillow绘制代码原生矢量形状与界面，使用时间函数计算真实逐帧动画；NumPy合成原创音乐与交互提示音；FFmpeg编码。
未调用Seedance、可灵、Runway等视频模型；未将图片平移冒称生成视频；没有第三方素材、歌曲或采样音轨。
图像和音轨均为此次案例制作，允许在此作品集内使用。Windows字体使用系统已安装的微软雅黑；字体文件不随交付分发。

复现环境
Windows + Python 3，Python 环境中已安装 Pillow（导入名 PIL）与 NumPy。
FFmpeg 和 FFprobe 需可从 PATH 调用；FFmpeg 需包含 libx264 视频编码器与 AAC 音频编码器。
需有系统微软雅黑字体 C:/Windows/Fonts/msyh.ttc 与 C:/Windows/Fonts/msyhbd.ttc。脚本使用这两个绝对字体路径；字体文件不随交付分发。

运行方式
在作品集根目录 byteintern-portfolio 中执行：
python evidence/motion/render-films.py both
也可切换到本 README 所在目录后执行：
python render-films.py both
将 both 换为 sync 或 light，可只渲染其中一条影片。

默认输出以 render-films.py 自身位置为基准，与启动命令的工作目录无关：
evidence/motion/renders/：重新生成的 MP4 与 JPG 封面。
evidence/motion/renders/evidence/：重新生成的关键帧联系表与 FFprobe JSON。
evidence/motion/renders/scratch/：合成声轨的中间 WAV 文件。
这些目录会自动创建，不覆盖 cases/motion 中已交付的影片或原有证据。
重复执行会替换上述 renders 目录中同名的重渲染文件。

可选路径参数（相对路径按当前工作目录解释，三个参数独立设置）：
python render-films.py both --out ./custom-renders --evidence ./custom-renders/evidence --scratch ./custom-renders/scratch

检查记录
FFprobe验证准确时长、帧数、画面规格及音轨；FFmpeg完整解码成功。
人工查看每片12个关键时间点，检查字形、主体遮挡、动作因果、整体风格和结尾阅读时间。
本证据不包含观众测试、实投表现、品牌审批或模型评测结果。
