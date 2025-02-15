import ezdxf
import math

def calculate_cutting_parameters(dxf_file):
    # Чтение DXF-файла
    doc = ezdxf.readfile(dxf_file)
    msp = doc.modelspace()

    total_length = 0.0
    total_area = 0.0

    # Множество для подсчета уникальных точек врезки
    unique_objects = set()

    # Обработка линий
    lines = []
    for line in msp.query('LINE'):
        start = (line.dxf.start.x, line.dxf.start.y)
        end = (line.dxf.end.x, line.dxf.end.y)
        length = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)  # Вычисляем длину
        total_length += length
        lines.append((start, end))  # Сохраняем начальную и конечную точки
        unique_objects.add(start)
        unique_objects.add(end)

    # Обработка кругов
    for circle in msp.query('CIRCLE'):
        radius = circle.dxf.radius
        area = math.pi * (radius ** 2)
        total_area += area
        total_length += 2 * math.pi * radius  # Длина окружности
        center = (circle.dxf.center.x, circle.dxf.center.y)
        unique_objects.add(center)

    # Обработка овальных прорезей
    for ellipse in msp.query('ELLIPSE'):
        a = ellipse.dxf.major_axis.length / 2  # Полуось по X
        b = ellipse.dxf.minor_axis.length / 2  # Полуось по Y
        area = math.pi * a * b
        total_area += area
        total_length += 2 * math.pi * math.sqrt((a**2 + b**2) / 2)  # Приближенная длина окружности овала
        center = (ellipse.dxf.center.x, ellipse.dxf.center.y)
        unique_objects.add(center)

    # Обработка многоугольников, представленных в виде линий
    if lines:
        # Создаем словарь для хранения вершин
        vertices = {}
        for start, end in lines:
            vertices[start] = vertices.get(start, 0) + 1
            vertices[end] = vertices.get(end, 0) + 1
            unique_objects.add(start)
            unique_objects.add(end)

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
    print(f"Количество уникальных точек врезки: {len(unique_objects)}")

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