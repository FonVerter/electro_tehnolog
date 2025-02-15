import ezdxf
import math

def calculate_cutting_parameters(dxf_file):
    # Чтение DXF-файла
    doc = ezdxf.readfile(dxf_file)
    msp = doc.modelspace()

    total_length = 0.0
    total_area = 0.0
    unique_objects = set()  # Для подсчета уникальных объектов

    # Обработка линий
    lines = []
    for line in msp.query('LINE'):
        start = line.dxf.start
        end = line.dxf.end
        length = math.sqrt((end.x - start.x) ** 2 + (end.y - start.y) ** 2)  # Вычисляем длину
        total_length += length
        lines.append((start, end))  # Сохраняем начальную и конечную точки

    # Обработка кругов
    for circle in msp.query('CIRCLE'):
        radius = circle.dxf.radius
        area = math.pi * (radius ** 2)
        total_area += area
        total_length += 2 * math.pi * radius  # Длина окружности
        unique_objects.add("circle")  # Добавляем уникальный объект

    # Обработка овальных прорезей
    for ellipse in msp.query('ELLIPSE'):
        center = ellipse.dxf.center
        a = ellipse.dxf.major_axis.length / 2  # Полуось по X
        b = ellipse.dxf.minor_axis.length / 2  # Полуось по Y
        area = math.pi * a * b
        total_area += area
        total_length += 2 * math.pi * math.sqrt((a**2 + b**2) / 2)  # Приближенная длина окружности овала
        unique_objects.add("oval")  # Добавляем уникальный объект

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
                    unique_objects.add("polygon")  # Добавляем уникальный объект

    # Вывод результатов
    print(f"Общая длина реза: {total_length:.2f} единиц")
    print(f"Общая площадь для вырезания: {total_area:.2f} квадратных единиц")
    print(f"Количество точек врезки: {len(unique_objects)}")

def calculate_polygon_area(vertices):
    """Функция для расчета площади многоугольника по координатам вершин."""
    area = 0.0
    n = len(vertices)
    for i in range(n):
        x1, y1 = vertices[i].x, vertices[i].y
        x2, y2 = vertices[(i + 1) % n].x, vertices[(i + 1) % n].y  # Следующая вершина, с учетом замыкания
        area += x1 * y2 - x2 * y1
    return abs(area) / 2.0

# Пример использования
calculate_cutting_parameters("C:\\Users\\FV\\Desktop\\python\\dxf-analyzer\\hardPart.DXF")


#кажется считает все четко. отсутствуют верные данные для точек врезки.