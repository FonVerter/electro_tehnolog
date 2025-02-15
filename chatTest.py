import ezdxf
import math
from pathlib import Path
from ezdxf import select

def calculate_cutting_parameters(dxf_file):
    # Чтение DXF-файла
    doc = ezdxf.readfile(dxf_file)
    msp = doc.modelspace()

    total_length = 0.0
    total_area = 0.0

    # Обработка линий
    lines = []
    for line in msp.query('LINE'):
        length = line.dxf.length
        total_length += length
        lines.append((line.dxf.start, line.dxf.end))  # Сохраняем начальную и конечную точки

    # Обработка кругов
    for circle in msp.query('CIRCLE'):
        radius = circle.dxf.radius
        area = math.pi * (radius ** 2)
        total_area += area
        total_length += 2 * math.pi * radius  # Длина окружности

    # Обработка многоугольников, представленных в виде линий
    if lines:
        # Создаем словарь для хранения вершин
        vertices = {}
        for start, end in lines:
            vertices[start] = vertices.get(start, 0) + 1
            vertices[end] = vertices.get(end, 0) + 1

        # Находим замкнутые многоугольники
        visited = set()
        for start, end in lines:
            if start not in visited:
                polygon = [start]
                current = end
                while current != start:
                    polygon.append(current)
                    visited.add(current)
                    # Ищем следующую линию, которая соединяет текущую точку
                    for next_start, next_end in lines:
                        if next_start == current and next_end not in visited:
                            current = next_end
                            break
                        elif next_end == current and next_start not in visited:
                            current = next_start
                            break
                    else:
                        break  # Если не нашли, выходим из цикла

                # Рассчитываем площадь многоугольника
                if len(polygon) > 2:  # Многоугольник должен иметь хотя бы 3 вершины
                    area = calculate_polygon_area(polygon)
                    total_area += area

    # Вывод результатов
    print(f"Общая длина реза: {total_length:.2f} единиц")
    print(f"Общая площадь для вырезания: {total_area:.2f} квадратных единиц")

def calculate_polygon_area(vertices):
    """Функция для расчета площади многоугольника по координатам вершин."""
    area = 0.0
    n = len(vertices)
    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]  # Следующая вершина, с учетом замыкания
        area += x1 * y2 - x2 * y1
    return abs(area) / 2.0

# Пример использования
calculate_cutting_parameters("D:\\squareCircle.DXF")