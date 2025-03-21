#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：SenseVoice 
@File    ：remote.py
@Author  ：chenyingtao
@Date    ：2025/3/19 17:59 
"""
"""
实现功能远程调用DeepSeek
"""
import re
from datetime import datetime
from zhipuai import ZhipuAI
from config.key import ZHIPUAI_API_KEY as ApiKey


def save_to_file(file, content, is_question=False):
    """保存对话内容到文件"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if is_question:
        file.write(f"\n[{timestamp}] Question:\n{content}\n\n[{timestamp}] Answer:\n")
    else:
        file.write(content)


def remote_infer(question: [], history=None):
    client = ZhipuAI(api_key=ApiKey)
    response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=[
            {"role": "user", "content": "你好"},
            {"role": "assistant", "content": "我是人工智能助手"},
            {"role": "user", "content": "你叫什么名字"},
            {"role": "user", "content": "我正在参加一个软件开发面试"},
            {"role": "user", "content": "输入的文本时语音转文字，存在一些字词误差，需要你纠正，按照软件开发常用的技术栈进行识别:常用名词如下"
                                        """
                                        软件开发涉及多种技术栈和专有名词，涵盖前端、后端、数据库、DevOps、云计算等多个领域。以下是一些常用的技术栈和专有名词：

### 1. **前端开发**
   - **HTML/CSS/JavaScript**：前端开发的基础技术。
   - **React**：由Facebook开发的前端JavaScript库。
   - **Vue.js**：轻量级的前端JavaScript框架。
   - **Angular**：由Google开发的前端JavaScript框架。
   - **TypeScript**：JavaScript的超集，增加了静态类型检查。
   - **Webpack**：模块打包工具，用于打包前端资源。
   - **Babel**：JavaScript编译器，用于将ES6+代码转换为兼容性更好的ES5代码。
   - **SASS/LESS**：CSS预处理器，增强CSS的功能。

### 2. **后端开发**
   - **Node.js**：基于Chrome V8引擎的JavaScript运行时，用于构建后端服务。
   - **Express.js**：Node.js的Web应用框架。
   - **Django**：Python的高级Web框架。
   - **Flask**：Python的轻量级Web框架。
   - **Spring Boot**：Java的微服务框架。
   - **Ruby on Rails**：Ruby的Web应用框架。
   - **ASP.NET Core**：微软开发的跨平台Web框架。
   - **GraphQL**：用于API的查询语言和运行时。
   - **RESTful API**：基于REST架构风格的API设计。

### 3. **数据库**
   - **MySQL**：开源的关系型数据库管理系统。
   - **PostgreSQL**：功能强大的开源关系型数据库。
   - **MongoDB**：NoSQL文档数据库。
   - **Redis**：开源的内存数据结构存储，常用作缓存。
   - **SQLite**：轻量级的嵌入式关系型数据库。
   - **Cassandra**：分布式的NoSQL数据库。
   - **Elasticsearch**：分布式搜索和分析引擎。

### 4. **DevOps**
   - **Docker**：容器化平台，用于打包和分发应用。
   - **Kubernetes**：容器编排工具，用于自动化部署、扩展和管理容器化应用。
   - **Jenkins**：开源的持续集成和持续交付工具。
   - **GitLab CI/CD**：集成在GitLab中的持续集成和持续交付工具。
   - **Ansible**：自动化配置管理和应用部署工具。
   - **Terraform**：基础设施即代码工具，用于自动化基础设施管理。
   - **Prometheus**：开源的系统监控和警报工具。
   - **Grafana**：开源的指标分析和可视化工具。

### 5. **云计算**
   - **AWS**：亚马逊云计算服务，提供多种云服务。
   - **Azure**：微软的云计算平台。
   - **Google Cloud Platform (GCP)**：谷歌的云计算平台。
   - **Heroku**：云平台即服务（PaaS），支持多种编程语言。
   - **DigitalOcean**：提供云服务器和基础设施的云服务提供商。

### 6. **版本控制**
   - **Git**：分布式版本控制系统。
   - **GitHub**：基于Git的代码托管平台。
   - **GitLab**：基于Git的代码托管和DevOps平台。
   - **Bitbucket**：基于Git的代码托管平台，由Atlassian提供。

### 7. **编程语言**
   - **JavaScript**：广泛用于前端和后端开发的脚本语言。
   - **Python**：通用编程语言，广泛用于Web开发、数据科学和人工智能。
   - **Java**：广泛用于企业级应用开发的编程语言。
   - **C#**：由微软开发的面向对象编程语言，广泛用于.NET平台。
   - **Ruby**：动态、面向对象的脚本语言，广泛用于Web开发。
   - **Go**：由Google开发的静态类型编程语言，适合并发编程。
   - **Rust**：系统编程语言，注重安全性和性能。
   - **Swift**：由Apple开发的编程语言，用于iOS和macOS应用开发。
   - **Kotlin**：由JetBrains开发的编程语言，广泛用于Android开发。

### 8. **测试**
   - **JUnit**：Java的单元测试框架。
   - **Selenium**：用于Web应用自动化测试的工具。
   - **Jest**：JavaScript的测试框架。
   - **Mocha**：JavaScript的测试框架。
   - **Cypress**：前端测试工具，用于端到端测试。
   - **Postman**：API测试工具。

### 9. **其他工具和技术**
   - **Nginx**：高性能的HTTP和反向代理服务器。
   - **Apache**：广泛使用的HTTP服务器。
   - **RabbitMQ**：开源的消息队列系统。
   - **Kafka**：分布式流处理平台。
   - **gRPC**：高性能的远程过程调用框架。
   - **WebSocket**：全双工通信协议，用于实时Web应用。
   - **OAuth**：开放授权标准，用于第三方应用访问用户数据。
   - **JWT**：JSON Web Token，用于安全的身份验证和信息交换。

### 10. **架构与设计模式**
   - **MVC**：模型-视图-控制器设计模式。
   - **MVVM**：模型-视图-视图模型设计模式。
   - **微服务架构**：将应用拆分为多个小型、独立的服务。
   - **单体架构**：传统的单一应用架构。
   - **事件驱动架构**：基于事件的系统设计。
   - **CQRS**：命令查询责任分离模式。
   - **DDD**：领域驱动设计。

### 总结
软件开发涉及的技术栈和专有名词非常广泛，涵盖了前端、后端、数据库、DevOps、云计算、版本控制、编程语言、测试、工具和技术、架构与设计模式等多个方面。掌握这些技术栈和名词有助于更好地理解和参与软件开发过程。"""
             },
            {"role": "user", "content": "请用简短的语言给出回答，分点讲述"},
            {"role": "assistant", "content": "我叫chatGLM"},
            {"role": "user", "content": question}
        ],
    )
    return dict(response.choices[0].message)['content']


def parse_completion_message(completion_message):
    # 提取 content 字段的内容
    content_match = re.search(r"content='(.*?)'", completion_message, re.DOTALL)
    content = content_match.group(1) if content_match else None

    # 提取 role 字段的内容
    role_match = re.search(r"role='(.*?)'", completion_message)
    role = role_match.group(1) if role_match else None

    # 提取 tool_calls 字段的内容（如果有）
    tool_calls_match = re.search(r"tool_calls=(.*?)(,|\))", completion_message)
    tool_calls = tool_calls_match.group(1) if tool_calls_match else None

    # 返回解析后的结果
    return {
        "content": content,
        "role": role,
        "tool_calls": tool_calls
    }


if __name__ == "__main__":
    text = "回答一下Redis 是什么？"
    question = [{'role': 'user', 'content': '嗯，你对java了解多少，请回答一下java中的多线程的创建方式。'}]
    text = remote_infer(question)
    answer = text
    print(dict(answer)["content"])
