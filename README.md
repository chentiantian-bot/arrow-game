# arrow-game
软件工程第二次个人作业——一箭又一箭小游戏
# README.md
# 项目名称：一箭又一箭（ArrowGame）
## 游戏简介
本项目是软件工程课程第二次个人作业，是使用 Python + Pygame 开发的点击式箭头解谜小游戏，开发过程借助AIGC工具辅助完成。
游戏棋盘为8×8网格，棋盘内放置上、下、左、右4种方向的箭头。玩家使用鼠标点击箭头，程序沿着箭头指向的方向检测路径：
1. 若箭头前进方向至棋盘边界之间**没有其他箭头阻挡**，箭头播放淡出动画并飞出棋盘消除；
2. 若路径上存在其他箭头，箭头无法消除，触发抖动动画作为碰撞反馈，同时消耗1次失误机会；
3. 每一关初始拥有3次失误次数，失误次数耗尽则本关失败；
4. 消除当前关卡内全部箭头，即可通关并自动进入下一关；
5. 游戏内置至少3个经过人工试玩验证、存在合法通关顺序的关卡；
6. 提供关卡重置按钮，可随时将当前关卡恢复至初始状态。

扩展附加功能：提示Hint功能、音效开关、动态移动小熊背景、按钮悬浮变色交互效果。

## 开发环境
- Python版本：Python 3.10 及以上
- 依赖库：pygame 2.5.0 及以上版本

## 安装和运行方法
1. 将项目仓库克隆到本地
```bash
git clone https://github.com/xxxx/arrow-game.git
cd arrow-game
```
2. 使用pip安装pygame依赖包
```bash
pip install pygame
```
3. 资源文件准备
将背景图片命名为`bear.jpg`，放置在项目根目录；音效文件`success.wav`、`fail.wav`同样放入项目根目录。
> 说明：图片、音效文件为可选素材，若缺失不会造成程序崩溃，程序会自动跳过素材加载。
4. 运行游戏
```bash
python main.py
```

## 游戏操作说明
1. 启动程序后，在**开始界面**点击【开始游戏】按钮，进入游戏对局界面。
2. 鼠标左键点击棋盘网格内的箭头，执行消除操作。
3. Restart按钮：重置当前关卡，箭头布局、剩余失误次数全部恢复为本关初始状态。
4. Hint按钮：高亮当前棋盘上可以直接消除的箭头，提供解谜提示。
5. Sound按钮：开启或者关闭游戏音效。
6. 通关规则：消除当前关卡棋盘上所有箭头，自动进入下一关。
7. 失败规则：失误次数耗尽时本关挑战失败，可点击Restart按钮重新游玩本关卡。

## 游戏截图
><img width="649" height="675" alt="image" src="https://github.com/user-attachments/assets/da5821e5-713d-4528-8fdc-2a5c44b01c97" /><img width="639" height="672" alt="image" src="https://github.com/user-attachments/assets/e44c5ce3-5c5d-4835-a30d-7d8834502ac7" /><img width="636" height="675" alt="image" src="https://github.com/user-attachments/assets/b9c73e72-09a9-4250-aac0-9af814378ac7" /><img width="626" height="665" alt="image" src="https://github.com/user-attachments/assets/c5b3b76b-d7d0-4907-9465-fe1797f17e6a" />





## 资源说明
1. `bear.jpg`：游戏背景图片，为本项目自定义素材。
2. `success.wav`、`fail.wav`：游戏音效，选用免费开源音效素材。
3. 源代码借助AIGC辅助生成，经过人工阅读、调试、修改与测试。

## Git提交记录
```
feat: 完成游戏棋盘和箭头显示
feat: 实现四个方向的路径检测
feat: 增加碰撞反馈和失误次数
feat: 增加关卡切换功能
fix: 修复向上检测时的数组越界
feat: 增加hint提示、音效、按钮hover
feat: 增加动态小熊背景
docs: 完善README和运行说明
```
<img width="907" height="236" alt="6b480ce0-8fb6-44a9-a25f-a3f11c42a157" src="https://github.com/user-attachments/assets/ddc51931-68e8-4ab1-b452-e14b4cf3ae79" />

## 项目文件结构
```
arrow-game/
├── main.py          # 游戏主源代码
├── README.md        # 项目说明文档
├── bear.jpg         # 背景图片资源
├── success.wav      # 成功消除音效
├── fail.wav         # 碰撞失败音效
```<img width="645" height="172" alt="image" src="https://github.com/user-attachments/assets/3cbf3d57-667e-4594-83d3-454d4d1d60ab" />
