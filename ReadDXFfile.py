import sys
import ezdxf
from pathlib import Path
from ezdxf import select

path_to_read_file = Path("C:\\Users\\FV\\Desktop\\python\\dxf-analyzer\\squareCircle.DXF")

try:
    doc = ezdxf.readfile(path_to_read_file)
    print('файл прочитан')
except IOError:
    print(f"Not a DXF file or a generic I/O error.")
    sys.exit(1)
except ezdxf.DXFStructureError:
    print(f"Invalid or corrupted DXF file.")
    sys.exit(2)

# получение пространства модели
msp = doc.modelspace()
# список объектов на 0 слое
zero_layer_objects = [entity for entity in msp if entity.dxf.layer == '0']
print('Количество объектов в файле вырезки: ' + str(len(zero_layer_objects)))
for primitive in zero_layer_objects:
    print(primitive)

# список окружностей
list_circe = [obj for obj in zero_layer_objects if obj.dxftype() == 'CIRCLE']

# Получаем диаметры
for circle in list_circe:
    radius = circle.dxf.radius
    center = circle.dxf.center
    #print(f"Тип объекта: {circle.dxftype()}, Диаметр: {round((radius*2), 2)}, Центр: {center}")

print("Количество отверстий: " + str(len(list_circe)) )
# список линий
list_line = [obj for obj in zero_layer_objects if obj.dxftype() == 'LINE']
print ('Количество линий: ' + str(len(list_line)))
print('-----------------------------------------------------------------------')



# координаты левый низ правый верх.bounding boxes
window = select.Window((-300, -300), (300, 300))
for entity in select.bbox_inside(window, msp):
    print(str(entity))

# пробуем делать коммиты и пуш 
#https://ezdxf.readthedocs.io/en/stable/tutorials/entity_selection.html выбор объекта на основании его положения






