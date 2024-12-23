import datetime
import random

def parse_dump(dump):
    packets = []

    for line in dump:
        parts = line.split()
        if not parts:  # Пропускаем пустые строки
            continue

        packet = {}

        # Время
        time_str = parts[0]
        sender_mac = parts[1]
        action = parts[5]
        target_mac = parts[3]

        # Определение типа пакета
        if "Request" in line:
            packet["type"] = "request"
            packet["target_ip"] = parts[10]
            packet["sender_ip"] = parts[12].strip(",")
        elif "Reply" in line:
            packet["type"] = "reply"
            packet["sender_ip"] = parts[8]
            packet["target_ip"] = parts[10].strip(",")

        # MAC-адреса
        packet["sender_mac"] = sender_mac
        packet["target_mac"] = target_mac.strip(",")

        # Преобразование времени в секунды
        time_obj = datetime.datetime.strptime(time_str, "%H:%M:%S.%f")
        packet["timestamp"] = (time_obj.hour * 3600 +
                                time_obj.minute * 60 +
                                time_obj.second +
                                time_obj.microsecond / 1_000_000)

        packets.append(packet)

    return packets

def count_replies_in_interval(packets, start_time, interval):
    reply_count = 0
    request_count = 0

    end_time = start_time + interval

    for packet in packets:
        if packet["type"] == "reply" and start_time <= packet["timestamp"] < end_time:
            reply_count += 1
        else:
            request_count += 1

    return reply_count, request_count


def main():
    # Чтение дампа ARP-пакетов из файла
    with open("file.out", "r") as file:
        dump = file.readlines()

    # Парсинг дампа
    packets = parse_dump(dump)

    # Интервал в секундах
    interval = 5

    # Выбор времени начала (в данном случае, начало первого пакета)
    start_time = packets[0]["timestamp"]

    # Подсчет ответов за интервал
    reply_count, request_count = count_replies_in_interval(packets, start_time, interval)

    print(f"Количество ответов ARP: {reply_count}, количество запросов ARP: {request_count} за интервал {interval} секунд")

if __name__ == "__main__":
    main()
