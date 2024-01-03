import json
import requests
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp
import schedule
import time

def main():
    # Modbus TCP配置
    modbus_host = '10.31.98.158'
    modbus_port = 502

    # API配置
    api_url = 'https://aisails.api.maev02.com/ess_cal/ess_status'
    api_headers = {'Content-Type': 'application/json'}

    # 读取Modbus数据
    try:
        # 创建Modbus TCP客户端
        master = modbus_tcp.TcpMaster(host=modbus_host, port=modbus_port, timeout_in_sec=1)
        master.set_timeout(1)

        # 执行Modbus读取
        # result = modbus_master.read_holding_registers(0x20, 20)
        result = master.execute(1, cst.READ_HOLDING_REGISTERS, 0x20, 20)

        # 将Modbus数据转换成JSON格式
        modbus_data = {
            'productName': 'DT Platn 1 Simulation',  # 请将这里替换为实际的产品名称
            'eticaBMS': {
                'soh': round(result[3] * 0.1, 1),
                'soc': round(result[2] * 0.1, 1),
                'totalVoltage': round(result[0] * 0.1, 1),
                'totalCurrent': round((result[1] - 20000) * 0.1, 1)
            }
        }

        # 打印Modbus数据
        print(f'Modbus Data: {modbus_data}')

        # 将Modbus数据写入JSON文件
        with open('ess_status_data.json', 'w', encoding='utf-8') as json_file:
            json.dump(modbus_data, json_file, indent=2)

        # 发送POST请求到API
        response = requests.post(api_url, json=modbus_data, headers=api_headers)

        # 打印API响应
        print(f'API Response: {response.json()}')

        # # 打印JavaScript风格的日志
        # formatted_date = 'YourFormattedDate'  # 请将这里替换为实际的日期
        # js_style_log = f"Recieve ESS data: {{ Name: {modbus_data['productName']}, SOC: {modbus_data['eticaBMS']['soc']}, totalVoltage: {modbus_data['eticaBMS']['totalVoltage']}, totalCurrent: {modbus_data['eticaBMS']['totalCurrent']} }} {formatted_date}"
        # print(js_style_log)

    except Exception as e:
        print(f'Error: {e}')

    finally:
        # 关闭Modbus连接
        master.close()


if __name__ == "__main__":
    # Schedule the main function to run every minute
    schedule.every(1).minutes.do(main)

    # Run the scheduled tasks indefinitely
    while True:
        schedule.run_pending()
        time.sleep(1)
    # main()