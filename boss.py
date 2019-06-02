from urllib import request, parse
import re
import json

class DataModel(object) :
    def __init__(self):
        self.title = ""
        self.salary = ""
        self.position = ""
        self.working_life = ""
        self.education = ""
        self.company_name = ""
        self.company_type = ""
        self.financing_info = ""
        self.staff_numbers = ""
        self.recruiter_name = ""
        self.recruiter_job = ""
        self.release_time = ""

def data_2_json(obj):
    return {
        "title" : obj.title,
        "salary" : obj.salary,
        "position" : obj.position,
        "working_life" : obj.working_life,
        "education" : obj.education,
        "company_name" : obj.company_name,
        "company_type" : obj.company_type,
        "financing_info" : obj.financing_info,
        "staff_numbers" : obj.staff_numbers,
        "recruiter_name" : obj.recruiter_name,
        "recruiter_job" : obj.recruiter_job,
        "release_time" : obj.release_time
    }


class Spider(object):
    def __init__(self):
        self.page = 1#页码
        self.switch = True
        self.data_list = []#数据列表

    def start_spider(self):
        while self.switch :
            self.load_page()
            command = input("是否继续爬取，是请按Y，否请按任意键")
            if command == "Y" or command == "y" :
                self.switch = True
                self.page += 1#爬取下一页
            else :
                self.switch = False
                self.page = 1
                self.data_list.clear()

    def load_page(self):
        #self.page=6
        """
        加载页面数据y
        """
        url_prefix = """https://www.zhipin.com/c100010000/h_100010000/?"""#url
        arg = {
            "query": "java",#搜索字
            "page": str(self.page),
            "ka": "page-" + str(self.page)
        }
        arg_str = parse.urlencode(arg)
        url = url_prefix + arg_str
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"}
        # 构建一个Request对象，填入URL和headers头信息
        my_request = request.Request(url=url, headers=headers)
        # 发送请求，获取服务器响应
        response = request.urlopen(my_request)
        html = response.read().decode("utf-8")
        # 观察HTML代码可以发现<ul><li><div class="job-list">...</div></li></ul>中包含我们需要的数据
        p_ul = re.compile(r"<ul>[\s]+<li>[\s]+<div\sclass=\"job-primary\">[\s\S]+</div>[\s]+</li>[\s]+</ul>")
        ul = p_ul.search(html)
        # 使用非贪婪模式获取到么一个li的数据
        p_li = re.compile(r"<li>[\s\S]+?<\/li>")
        content_list = p_li.findall(ul.group())
        self.deal_page(content_list)
        self.write_page()

    def deal_page(self, content_list) :
        """
        处理页面中的数据
        :param content_list:所有数据，带有HTML标签
        """
        for content in content_list :
            # 基本信息
            p_primary_content = re.compile(r"<div\sclass=\"info-primary\">[\s\S]+?</div>[\s\S]+?</div>[\s\S]+?</div>")
            primary_content = p_primary_content.search(str(content)).group()
            # 公司信息
            p_company_content = re.compile(r"<div\sclass=\"info-company\">[\s\S]+?</div>[\s\S]+?</div>")
            company_content = p_company_content.search(str(content)).group()
            # 其他信息
            p_other_content = re.compile(r"<div\sclass=\"info-publis\">[\s\S]+?</div>")
            other_content = p_other_content.search(str(content)).group()

            # 创建各个数据的匹配规则
            p_title = re.compile(r"<div class=\"job-title\">(.+)</div>")
            p_salary = re.compile(r"<span class=\"red\">(.+)</span>")
            p_position = re.compile(r"<p>(.+?)<em\sclass=\"vline\">")
            p_working_life = re.compile(r"</em>(.+?)<em\sclass=\"vline\">")
            p_education = re.compile(r"</em>((?!<em\sclass=\"vline\"></em>).)*</p>")
            p_company_name = re.compile(r"<h3 class=\"name\">(.+)</h3>")
            p_company_type = re.compile(r"<p>(.+?)<em\sclass=\"vline\">")
            p_financing_info = re.compile(r"</em>(.+?)<em\sclass=\"vline\">")
            p_staff_numbers = re.compile(r"</em>((?!<em\sclass=\"vline\"></em>).)*</p>")
            p_recruiter_name = re.compile(r"<h3 class=\"name\">(.+)<em class=\"vline\">")
            p_recruiter_job = re.compile(r"</em>(.+?)</h3>")
            p_release_time = re.compile(r"<p>(.+?)</p>")

            # 所有数据
            data = DataModel()
            data.title = self.get_data(p_title, primary_content)
            data.salary = self.get_data(p_salary, primary_content)
            data.position = self.get_data(p_position, primary_content)
            data.working_life = self.get_data(p_working_life, primary_content)
            data.education = self.get_data(p_education, primary_content)
            data.company_name = self.get_data(p_company_name, company_content)
            data.company_type = self.get_data(p_company_type, company_content)
            data.financing_info = self.get_data(p_financing_info, company_content)
            data.staff_numbers = self.get_data(p_staff_numbers, company_content)
            data.recruiter_name = self.get_data(p_recruiter_name, other_content)
            data.recruiter_job = self.get_data(p_recruiter_job, other_content)
            data.release_time = self.get_data(p_release_time, other_content)
            self.data_list.append(data)

    def del_tag(self, content):
        """
        去掉HTML标签
        :param content: 还有HTML标签的文本
        :return: 去掉HTML标签的文本
        """
        p_del_tag = re.compile(r"<(.+?)>", re.S)
        return p_del_tag.sub("", content)

    def get_data(self, pattern, content):
        """
        获取有效的数据
        :param pattern: 正则匹配表达式
        :param content: 需要匹配的文本
        :return: 去掉标签的有效数据
        """
        tag_data = pattern.search(str(content))
        if tag_data :
            return self.del_tag(tag_data.group())
        else :
            return "暂无信息"

    def write_page(self):
        """
        将数据写入文件
        """
        with open("招聘信息" + str(self.page) + ".txt", "a") as f:
            #print("title", ",","salary",",", "position",",", "working_life", ",","education", ",","company_name",",",
             #     "company_type",",", "financing_info",",", "staff_numbers", ",","recruiter_name",",",
              #    "recruiter_job", ",","release_time")
            for data in self.data_list :
                object=json.dumps(data, default=data_2_json, ensure_ascii=False)
                your_dict = json.loads(object)

                print(your_dict["title"]+","+your_dict["salary"]+","+your_dict["position"][0:2]+","+
                      your_dict["working_life"]+","+your_dict["education"]+","+your_dict["company_name"]+","+
                      your_dict["company_type"]+","+your_dict["financing_info"]+","+your_dict["staff_numbers"]+","+
                      your_dict["recruiter_name"]+","+your_dict["recruiter_job"]+","+your_dict["release_time"])
                #f.write(object)
                #f.write("\n")
            self.data_list.clear()

if __name__ == '__main__':
    spider = Spider()
    spider.start_spider()
