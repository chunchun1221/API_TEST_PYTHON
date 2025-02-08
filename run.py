import os
import pytest
from datetime import datetime
from config.settings import BASE_DIR

if __name__ == "__main__":
    # 创建报告目录
    report_dir = os.path.join(BASE_DIR, 'reports', 'allure_results')
    os.makedirs(report_dir, exist_ok=True)

    # 生成时间戳
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 运行 pytest 并生成 Allure 结果文件
    pytest.main([
        "-v",  # 显示详细日志
        "--alluredir", report_dir,  # 指定 Allure 结果文件目录
        "test_cases/"  # 测试用例目录
    ])

    # 生成 Allure 报告（固定目录名）
    allure_report_dir = os.path.join(BASE_DIR, 'reports', 'allure-report')
    os.system(f"allure generate {report_dir} -o {allure_report_dir} --clean")

    # 打开 Allure 报告
    os.system(f"allure open {allure_report_dir}")