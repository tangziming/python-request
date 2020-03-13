import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s :: %(levelname)s :: %(filename)s :: %(funcName)s :: %(lineno)d] %(message)s',
    filename='testlog.txt',
    filemode='a'
)



if __name__=='__main__':
    logging.debug("hello")
    logging.info("hello")
    logging.warning("hello")
    logging.error("hello")
    logging.critical("hello")


def log_case_info(case_name , url , data , res_dict):
    logging.info("测试用例：{}".format(case_name))
    logging.info("url：{}".format(url))
    logging.info("请求参数：{}".format(data))
    logging.info("实际结果：{}".format(res_dict))
