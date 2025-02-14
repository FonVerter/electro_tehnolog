import sys
import ezdxf

try:
    doc = ezdxf.readfile("D:\\kompas_marco\\dxfAnalyzer\\circleSquareRectangle.DXF")
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



# пробуем делать коммиты и пуш






