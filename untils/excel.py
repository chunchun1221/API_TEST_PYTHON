from pathlib import Path
import os
import pandas as pd
from untils.logger import logger


class ExcelUtil(object):
    def __init__(self, file_path=None):
        if file_path is None:
            try:
                # 使用项目根目录作为基准路径
                project_root = Path(__file__).resolve().parents[1]  # 获取 untils 的上一层目录
                default_file_path = project_root / 'data' / 'casedata.xlsx'

                logger.info("文件路径为空, 将使用默认路径")
                logger.info(f"默认文件路径为: {default_file_path}")

                self.file_path = str(default_file_path)
            except Exception as e:
                logger.error(f"生成默认文件路径失败: {e}")

        else:
            self.file_path = file_path

    def read_excel(self, sheet_name=None, use_cols=None, skip_rows=None, chunk_size=None):
        try:
            if chunk_size:
                # 分块读取数据
                for chunk in pd.read_excel(self.file_path, sheet_name=sheet_name, usecols=use_cols, skiprows=skip_rows, chunksize=chunk_size):
                    yield chunk
                    logger.info(f"读取excel成功, sheet_name: {sheet_name}, use_cols: {use_cols}, skip_rows: {skip_rows}, chunk_size: {chunk_size}")
            else:
                # 读取所有数据并过滤掉空白行
                df = pd.read_excel(self.file_path, sheet_name=sheet_name, usecols=use_cols, skiprows=skip_rows)
                df.dropna(how='any', inplace=True)  # 在读取时直接过滤掉空白行
                for _, row in df.iterrows():
                    yield row
                    logger.info(f"读取excel成功, sheet_name: {sheet_name}, use_cols: {use_cols}, skip_rows: {skip_rows}")
        except Exception as e:
            logger.error(f"{e}, 读取excel失败, sheet_name: {sheet_name}, use_cols: {use_cols}, skip_rows: {skip_rows}, chunk_size: {chunk_size}")

    def clean_data(self, df_generator):
        for df in df_generator:
            if isinstance(df, pd.DataFrame):
                # 对于分块读取的DataFrame块，直接产出
                for _, row in df.iterrows():
                    yield row
            elif isinstance(df, pd.Series):
                # 对于普通读取生成的每行数据（Series类型），若不是空白行则产出
                if not df.isnull().any():
                    yield df
            else:
                logger.warning("未知的数据类型，跳过处理")


if __name__ == "__main__":
    excel_util = ExcelUtil()
    sheet_name = 'Login'
    use_cols = ['账号名', '密码', '预期结果定位', '预期结果']
    data_generator = excel_util.read_excel(sheet_name=sheet_name, use_cols=use_cols)
    for row in excel_util.clean_data(data_generator):
        print(row)
