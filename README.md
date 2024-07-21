# 汉朔接入点自动化配置软件   
Hanshow AP Automation Configuration Software

## 项目概述
用于配置和管理 AP 网络的工具。该工具使用 PyQt5 构建图形用户界面，提供了对 AP 网络的自动搜索和配置功能。

## 核心功能
- **网络扫描与 AP 发现**：自动扫描当前网络，识别所有在线的 AP 设备。
- **网络配置管理**：提供直观的 GUI 界面来配置 AP 的 IP 地址、子网掩码、网关和 DNS 等网络参数。
- **ESL 配置**：设置 ESL 工作地址与端口，支持自动搜索和手动配置模式。
- **测试模式管理**：启用或禁用 AP 的测试模式，配置测试参数。
- **配置文件管理**：支持从预定义的配置文件中读取和应用配置。
- **设备详情与配置**：查看并修改 AP 的详细配置，将在后续版本支持批量操作。

## 项目结构
- `main.py`：主应用程序入口，包含 GUI 初始化和事件处理逻辑。
- `model.py`：封装网络操作和 AP 配置相关的核心逻辑。
- `utils.py`：提供实用工具函数，如 MD5 加密、IP 地址验证和转换等。
- `config/`：存储 AP 配置文件的目录。
- `style/`：存储应用程序的样式资源和图标。
- `build/`：构建和打包相关文件（可根据需要删除）。
- `lib/`：包含其他依赖库和模块。

## 环境要求
- Python 版本：3.6+
- 依赖库：PyQt5、paramiko、pandas

## 安装指南

### 安装依赖
在项目根目录下执行以下命令安装所有必要的依赖：
```bash
pip install -r requirements.txt
```
或者单独为其创建一个python虚拟环境用于割离主要的python环境
```python
python -m venv env310(可自行修改)
.\env310\Scripts\activate #激活并使用虚拟环境
pip install -r requirements.txt #下载依赖包库
```
