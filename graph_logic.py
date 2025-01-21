import matplotlib.pyplot as plt
import heapq

class Vertex:
    def __init__(self, node, coordinates):
        self.id = node
        self.adjacent = {}
        self.coordinates = coordinates

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def get_coordinates(self):
        return self.coordinates


class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node, coordinates):
        self.num_vertices += 1
        new_vertex = Vertex(node, coordinates)  # Передаємо координати при створенні вершини
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, speed=0, distance=0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], (speed, distance))
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], (speed, distance))

    def get_vertices(self):
        return self.vert_dict.keys()


class GraphVisual:
    def __init__(self, graph):
        self.graph = graph

    def visualize(self):
        plt.figure(figsize=(10, 8))

        # Малювання ребер
        for vertex in self.graph:
            for neighbor in vertex.get_connections():
                # Отримуємо координати вершин та сусідів
                x1, y1 = vertex.get_coordinates()
                x2, y2 = neighbor.get_coordinates()

                # Малюємо лінію між вершинами
                plt.plot([x1, x2], [y1, y2], 'k-', lw=0.7)

        # Малювання вершин
        for vertex in self.graph:
            x, y = vertex.get_coordinates()
            plt.plot(x, y, 'go', markersize=10)
            plt.text(x, y + 0.1, str(vertex.get_id()), ha='center', fontsize=7)

        plt.axis('off')
        plt.show()

class ShortestPath:
    def __init__(self, graph):
        self.graph = graph

    def dijkstra(self, start, end):

        '''distances — словник, де ключ — вершина, значення — найкоротша відома відстань від початкової вершини
        до цієї (на початку — нескінченність для всіх, крім стартової вершини).'''
        distances = {vertex: float('inf') for vertex in self.graph.get_vertices()}

        '''previous — словник для збереження попередників вершин у найкоротшому шляху.'''
        previous = {vertex: None for vertex in self.graph.get_vertices()}

        distances[start] = 0

        '''priority_queue — черга з пріоритетом, яка зберігає вершини для обробки. Пріоритетом є вага.'''
        priority_queue = [(0, start)]  # (вага, вершина)

        '''
        Головний цикл алгоритму Дейкстри:
        Цикл працює доти, поки черга з пріоритетом (priority_queue) не стане порожньою.
        Черга містить вершини, які ще потрібно обробити. Кожна вершина має вагу (час досягнення від початкової вершини).
        Витягуємо вершину з найменшою вагою (часом) із черги.
        current_distance — мінімальний час досягнення вершини current_vertex з усіх оброблених на даний момент.
        Модуль heapq реалізує чергу з пріоритетом, яка автоматично підтримує впорядкованість елементів. 
        Найменший елемент завжди опиняється на початку.
        
        Якщо поточна вершина є кінцевою (end), то ми завершили пошук і виходимо з циклу.
        У алгоритмі Дейкстри, перше досягнення кінцевої вершини гарантує, що знайдений шлях є найкоротшим 
        (оскільки всі вершини в черзі розглядаються у порядку зростання їхньої ваги).
        
        Обхід сусідніх вершин:
        Отримуємо всіх сусідів поточної вершини current_vertex.
        Сусіди — це вершини, з'єднані ребрами з current_vertex.
        Знаходимо характеристики ребра між current_vertex і neighbor:
        distance — відстань між вершинами.
        speed — швидкість руху по цьому ребру.
        Розраховуємо вагу ребра (weight) у вигляді часу (distance / speed).
        Для алгоритму Дейкстри вага кожного ребра повинна бути заздалегідь відомою. У нашому випадку вагою є час.
        Обчислюємо потенційну нову відстань до сусідньої вершини через поточну вершину:
        current_distance — мінімальний час досягнення поточної вершини.
        weight — час переходу до сусідньої вершини.
        Результат (new_distance) показує, наскільки швидше ми можемо дістатися до neighbor.
        
        Перевіряємо, чи нова відстань до сусідньої вершини (new_distance) менша за поточну відому відстань 
        (distances[neighbor.get_id()]).
        Якщо так:
        Оновлюємо відстань до сусіда в словнику distances.
        Зберігаємо попередню вершину (current_vertex) у словнику previous, щоб зберегти маршрут.
        Додаємо сусіда до черги з його новою вагою.
        
        Використовуємо словник previous для відновлення маршруту:
        Починаємо з кінцевої вершини (end).
        Вставляємо вершини на початок списку path, проходячи по ланцюгу попередників.
        Коли current стає None, ми досягли початкової вершини (start).
        Повертаємо:
        path — список вершин, які складають найкоротший шлях.
        distances[end] — мінімальний час, необхідний для досягнення кінцевої вершини.   
        '''

        while priority_queue:
            current_distance, current_vertex = heapq.heappop(priority_queue)

            # Якщо знайшли кінцеву вершину — зупиняємось
            if current_vertex == end:
                break

            for neighbor in self.graph.get_vertex(current_vertex).get_connections():
                speed, distance = self.graph.get_vertex(current_vertex).get_weight(neighbor)
                weight = distance / speed  # Час = відстань / швидкість
                new_distance = current_distance + weight

                if new_distance < distances[neighbor.get_id()]:
                    distances[neighbor.get_id()] = new_distance
                    previous[neighbor.get_id()] = current_vertex
                    heapq.heappush(priority_queue, (new_distance, neighbor.get_id()))

        path, current = [], end
        while current is not None:
            path.insert(0, current)
            current = previous[current]
        return path, distances[end]

    def visual_path(self, path):
        '''
        Функція має на меті малювати граф із виділенням шляху, переданого у вигляді списку вузлів (вершин).
        Ось як працює кожна частина:
        '''

        plt.figure(figsize=(10, 8))

        '''
        Цей код ітерує по всіх вершинах графа (self.graph). Для кожної вершини ми перевіряємо її з'єднання (сусідів), 
        отримуючи їх координати за допомогою методу get_coordinates().
        '''
        for vertex in self.graph:
            for neighbor in vertex.get_connections():
                x1, y1 = vertex.get_coordinates()
                x2, y2 = neighbor.get_coordinates()

                '''
                Перевірка, чи належать поточні вершини до шляху. Якщо обидві вершини (поточна та її сусід) 
                входять до списку path, ми розглядаємо це ребро як частину шляху.
                Додатково перевіряється, чи є ці дві вершини сусідніми в шляху (тобто їх індекси відрізняються на 1).
                Якщо так, ребро малюється зеленим (яке є частиною шляху).
                Якщо ні, малюється чорним (це ребро, але не частина шляху).
                Якщо хоча б одна з вершин не входить до шляху, малюється чорне ребро.
                '''
                if vertex.get_id() in path and neighbor.get_id() in path:
                    if abs(path.index(vertex.get_id()) - path.index(neighbor.get_id())) == 1:
                        plt.plot([x1, x2], [y1, y2], 'g-', lw=3)
                    else:
                        plt.plot([x1, x2], [y1, y2], 'k-', lw=0.7)
                else:
                    plt.plot([x1, x2], [y1, y2], 'k-', lw=0.7)

        # Малювання вершин
        for vertex in self.graph:
            x, y = vertex.get_coordinates()

            # Якщо місто на шляху, робимо точку іншого кольору
            if vertex.get_id() in path:
                plt.plot(x, y, 'bo', markersize=10)
            else:
                plt.plot(x, y, 'co', markersize=10)

            plt.text(x, y + 0.1, str(vertex.get_id()), ha='center', fontsize=7)

        plt.axis('off')
        plt.show()

# ----------------------------------------------------------------------------------------------------------------------

def add_cities(g):

    g.add_vertex('Лісабон', (0.25, 0.67))
    g.add_vertex('Порто', (0.39, 2.01))
    g.add_vertex('Мадрид', (1.80, 1.60))
    g.add_vertex('Барселона', (3.48, 2.13))
    g.add_vertex('Будапешт', (8.00, 5.20))
    g.add_vertex('Марсель', (4.39, 3.18))
    g.add_vertex('Париж', (3.53, 6.24))
    g.add_vertex('Берлін', (6.69, 8.25))
    g.add_vertex('Мілан', (5.48, 4.38))
    g.add_vertex('Брюсель', (4.10, 7.34))
    g.add_vertex('Амстердам', (4.26, 8.17))
    g.add_vertex('Гамбург', (5.71, 8.82))
    g.add_vertex('Франкфурт', (5.34, 6.93))
    g.add_vertex('Мюнхен', (6.17, 5.84))
    g.add_vertex('Рим', (6.43, 2.42))
    g.add_vertex('Прага', (6.98, 6.91))
    g.add_vertex('Цюрих', (5.30, 5.43))
    g.add_vertex('Відень', (7.54, 5.88))
    g.add_vertex('Варшава', (8.86, 8.09))
    g.add_vertex('Братислава', (7.74, 5.85))
    g.add_vertex('Любляна', (7.00, 4.70))
    g.add_vertex('Загреб', (7.42, 4.57))
    g.add_vertex('Брно', (7.60, 6.43))
    g.add_vertex('Краков', (8.56, 6.90))
    g.add_vertex('Гданськ', (8.18, 9.26))
    g.add_vertex('Бухарест', (10.32, 3.81))
    g.add_vertex('Софія', (9.52, 2.86))
    g.add_vertex('Афіни', (9.64, 0.27))
    g.add_vertex('Копенгаген', (6.45, 9.99))

def add_edges(g):

    g.add_edge('Марсель', 'Париж', 110, 775)
    g.add_edge('Марсель', 'Рим', 105, 720)
    g.add_edge('Марсель', 'Мілан', 95, 410)
    g.add_edge('Марсель', 'Мадрид', 110, 775)
    g.add_edge('Марсель', 'Барселона', 110, 375)
    g.add_edge('Порто', 'Барселона', 110, 625)
    g.add_edge('Порто', 'Мадрид', 110, 325)
    g.add_edge('Порто', 'Лісабон', 110, 235)
    g.add_edge('Мадрид', 'Лісабон', 110, 535)
    g.add_edge('Барселона', 'Лісабон', 110, 735)
    g.add_edge('Рим', 'Мілан', 85, 570)
    g.add_edge('Париж', 'Берлін', 100, 1050)
    g.add_edge('Париж', 'Барселона', 100, 850)
    g.add_edge('Париж', 'Мадрид', 100, 950)
    g.add_edge('Париж', 'Брюсель', 110, 180)
    g.add_edge('Париж', 'Франкфурт', 120, 350)
    g.add_edge('Париж', 'Цюрих', 130, 450)
    g.add_edge('Барселона', 'Мадрид', 100, 350)
    g.add_edge('Берлін', 'Мілан', 95, 850)
    g.add_edge('Берлін', 'Варшава', 120, 450)
    g.add_edge('Берлін', 'Франкфурт', 120, 350)
    g.add_edge('Мілан', 'Брюсель', 90, 600)
    g.add_edge('Брюсель', 'Амстердам', 110, 170)
    g.add_edge('Амстердам', 'Гамбург', 85, 460)
    g.add_edge('Амстердам', 'Франкфурт', 85, 215)
    g.add_edge('Гамбург', 'Франкфурт', 120, 490)
    g.add_edge('Гамбург', 'Копенгаген', 80, 330)
    g.add_edge('Гамбург', 'Берлін', 150, 290)
    g.add_edge('Гамбург', 'Мюнхен', 130, 780)
    g.add_edge('Франкфурт', 'Мюнхен', 110, 390)
    g.add_edge('Мюнхен', 'Рим', 100, 1180)
    g.add_edge('Мюнхен', 'Мілан', 105, 600)
    g.add_edge('Мюнхен', 'Любляна', 115, 380)
    g.add_edge('Мюнхен', 'Цюрих', 115, 180)
    g.add_edge('Мюнхен', 'Відень', 115, 135)
    g.add_edge('Прага', 'Цюрих', 75, 530)
    g.add_edge('Прага', 'Мюнхен', 85, 380)
    g.add_edge('Прага', 'Берлін', 120, 350)
    g.add_edge('Прага', 'Брно', 85, 200)
    g.add_edge('Прага', 'Гданськ', 105, 550)
    g.add_edge('Прага', 'Варшава', 95, 340)
    g.add_edge('Прага', 'Краков', 115, 370)
    g.add_edge('Прага', 'Франкфурт', 125, 510)
    g.add_edge('Прага', 'Любляна', 105, 520)
    g.add_edge('Прага', 'Відень', 155, 330)
    g.add_edge('Краков', 'Брно', 95, 210)
    g.add_edge('Краков', 'Варшава', 120, 300)
    g.add_edge('Гданськ', 'Варшава', 120, 340)
    g.add_edge('Гданськ', 'Берлін', 130, 280)
    g.add_edge('Гданськ', 'Гамбург', 110, 470)
    g.add_edge('Цюрих', 'Відень', 85, 660)
    g.add_edge('Цюрих', 'Мілан', 85, 230)
    g.add_edge('Цюрих', 'Марсель', 115, 295)
    g.add_edge('Цюрих', 'Франкфурт', 115, 215)
    g.add_edge('Братислава', 'Відень', 115, 60)
    g.add_edge('Братислава', 'Загреб', 125, 380)
    g.add_edge('Братислава', 'Брно', 135, 130)
    g.add_edge('Варшава', 'Братислава', 80, 330)
    g.add_edge('Любляна', 'Загреб', 45, 130)
    g.add_edge('Любляна', 'Мілан', 75, 490)
    g.add_edge('Любляна', 'Рим', 120, 290)
    g.add_edge('Загреб', 'Брно', 50, 320)
    g.add_edge('Краков', 'Гданськ', 90, 430)
    g.add_edge('Будапешт', 'Бухарест', 100, 380)
    g.add_edge('Будапешт', 'Загреб', 115, 340)
    g.add_edge('Будапешт', 'Братислава', 105, 200)
    g.add_edge('Рим', 'Загреб', 120, 600)
    g.add_edge('Рим', 'Будапешт', 120, 850)
    g.add_edge('Краков', 'Будапешт', 120, 400)
    g.add_edge('Бухарест', 'Софія', 120, 300)
    g.add_edge('Афіни', 'Софія', 120, 310)
    g.add_edge('Загреб', 'Софія', 120, 510)
    g.add_edge('Афіни', 'Бухарест', 105, 600)
    g.add_edge('Будапешт', 'Софія', 180, 350)

def get_user_input():
    start_city = input("Введіть назву початкового міста: ")
    end_city = input("Введіть назву кінцевого міста: ")
    return start_city, end_city

def find_shortest_path(g, start_city, end_city):
    sp = ShortestPath(g)
    if g.get_vertex(start_city) and g.get_vertex(end_city):
        path, time = sp.dijkstra(start_city, end_city)
        print(f"Найкоротший шлях: {' -> '.join(path)}")
        print(f"Загальний час у дорозі: {time:.2f} годин")
        sp.visual_path(path)
    else:
        print("Одне з введених міст не існує!")

def main():
    g = Graph()

    add_cities(g)
    add_edges(g)

    gv = GraphVisual(g)
    gv.visualize()

    start_city, end_city = get_user_input()

    find_shortest_path(g, start_city, end_city)

if __name__ == '__main__':

    main()
