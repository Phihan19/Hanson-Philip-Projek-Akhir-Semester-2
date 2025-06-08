# Import pustaka yang dibutuhkan
import heapq        # Untuk struktur data antrian prioritas, dipakai di algoritma Dijkstra
import itertools    # Untuk mencoba semua kemungkinan rute dalam TSP
import matplotlib.pyplot as plt  # Untuk menggambar peta/grafik kota
import networkx as nx            # Untuk membangun graf jaringan kota

# Kelas utama yang merepresentasikan peta kota dan koneksinya
class CityMap:
    def __init__(self):     # Menyimpan graf terpisah untuk setiap moda transportasi
        self.graphs = {
            'mobil': {},
            'motor': {},
            'jalan_kaki': {}
        }

    def add_vertex(self, city):     # Menambahkan kota ke setiap moda, jika belum ada
        for mode in self.graphs:
            if city not in self.graphs[mode]:
                self.graphs[mode][city] = []

    def add_edge(self, city1, city2, distances):      # Menambahkan jalur dua arah (karena bisa bolak-balik)
        for mode in self.graphs:
            self.graphs[mode][city1].append((city2, distances[mode]))
            self.graphs[mode][city2].append((city1, distances[mode]))

    def get_vertices(self):       # Mengambil semua nama kota dari salah satu graf (semua graf pasti punya data kota yang sama)
        return list(self.graphs['mobil'].keys())

    def dijkstra(self, mode, start, end):       # Mencari jalur tercepat dari kota A ke B menggunakan Dijkstra
        graph = self.graphs[mode]
        heap = [(0, start, [])]  
        visited = set()

        while heap:
            cost, city, path = heapq.heappop(heap)
            if city in visited:
                continue  # Lewati jika kota sudah dikunjungi
            visited.add(city)
            path = path + [city]

            if city == end:
                return path, cost  # Ketemu tujuan, selesai!

            # Cek semua kota tetangga dari kota saat ini
            for neighbor, weight in graph[city]:
                if neighbor not in visited:
                    heapq.heappush(heap, (cost + weight, neighbor, path))

        return None, float("inf")  # Kalau tidak ada rute ke tujuan

    def tsp_brute_force(self, mode):       # Mencari rute terbaik yang mengunjungi semua kota sekali saja
        graph = self.graphs[mode]
        cities = self.get_vertices()
        min_path = None
        min_distance = float("inf")

        # Mencoba semua urutan perjalanan yang mungkin (permutasi)
        for perm in itertools.permutations(cities):
            distance = 0
            valid = True

            for i in range(len(perm) - 1):
                src = perm[i]
                dst = perm[i + 1]

                # Cek apakah ada jalur langsung dari kota asal ke kota tujuan
                for neighbor, weight in graph[src]:
                    if neighbor == dst:
                        distance += weight
                        break
                else:
                    valid = False  # Permutasi dibatalkan jika idak ada jalur langsung
                    break

            if valid and distance < min_distance:
                min_distance = distance
                min_path = perm  # Menyimpan rute terbaik sejauh ini

        return min_path, min_distance

# Gambar graf kota beserta jalurnya
def draw_city_graph(graph_obj, mode, tsp_path=None, dijkstra_path=None):
    graph = graph_obj.graphs[mode]
    G = nx.Graph()

    # Bangun graf dari data
    for city in graph:
        G.add_node(city)
        for neighbor, weight in graph[city]:
            if not G.has_edge(city, neighbor):
                G.add_edge(city, neighbor, weight=weight)

    # Posisi kota secara relatif terhadap peta Jawa
    pos = {
        "Jakarta": (0, 3), "Tangerang": (-0.3, 2.6), "Depok": (0.5, 2.8), "Bogor": (0.7, 2.2), "Bekasi": (0.9, 3.2),
        "Bandung": (2.2, 2), "Cirebon": (3.5, 2.5), "Semarang": (5, 3), "Yogyakarta": (6.3, 2.4), "Surabaya": (8, 3)
    }

    # Gambar simpul (kota), label kota, dan jalur antar kota
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightgreen')
    nx.draw_networkx_labels(G, pos, font_size=9)
    nx.draw_networkx_edges(G, pos, width=1, edge_color='gray')

    # Menambahkan label jarak antar kota
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)

    # Jika ada jalur TSP, jalur berwarna merah
    if tsp_path:
        tsp_edges = [(tsp_path[i], tsp_path[i + 1]) for i in range(len(tsp_path) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=tsp_edges, edge_color='red', width=2)

    # Jika ada jalur tercepat (Dijkstra), jalur berwarna biru putus-putus
    if dijkstra_path:
        dijkstra_edges = [(dijkstra_path[i], dijkstra_path[i + 1]) for i in range(len(dijkstra_path) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=dijkstra_edges, edge_color='blue', width=2, style='dashed')

    plt.title(f"Peta Kota Jawa - Mode: {mode.capitalize()}\nMerah = TSP, Biru Putus = Dijkstra", fontsize=12)
    plt.axis('off')  
    plt.tight_layout()
    plt.show()

# ========== PROGRAM UTAMA ==========
# Buat peta dan daftar kota
city_map = CityMap()
cities = ["Jakarta", "Bogor", "Depok", "Tangerang", "Bekasi", "Bandung", "Cirebon", "Semarang", "Yogyakarta", "Surabaya"]

# Menambahkan semua kota ke dalam graf
for city in cities:
    city_map.add_vertex(city)

# Daftar koneksi antar kota dan jaraknya (30 edge)
base_edges = [
    ("Jakarta", "Bogor", 60), ("Jakarta", "Depok", 35), ("Jakarta", "Tangerang", 30),
    ("Jakarta", "Bekasi", 40), ("Bogor", "Bandung", 120), ("Depok", "Bekasi", 25),
    ("Tangerang", "Cirebon", 270), ("Bekasi", "Bandung", 140), ("Bandung", "Cirebon", 130),
    ("Cirebon", "Semarang", 220), ("Semarang", "Yogyakarta", 130), ("Yogyakarta", "Surabaya", 330),
    ("Bandung", "Semarang", 350), ("Bogor", "Cirebon", 300), ("Depok", "Semarang", 370),
    ("Bekasi", "Cirebon", 200), ("Depok", "Bandung", 130), ("Tangerang", "Bandung", 160),
    ("Bogor", "Semarang", 340), ("Tangerang", "Semarang", 400), ("Cirebon", "Yogyakarta", 250),
    ("Bandung", "Yogyakarta", 300), ("Bekasi", "Semarang", 360), ("Depok", "Yogyakarta", 410),
    ("Jakarta", "Cirebon", 280), ("Jakarta", "Bandung", 150), ("Tangerang", "Yogyakarta", 450),
    ("Bogor", "Yogyakarta", 370), ("Cirebon", "Surabaya", 500), ("Semarang", "Surabaya", 350)
]

# Menambahkan edge ke graf untuk setiap moda transportasi, dengan konversi jarak
for src, dst, dist in base_edges:
    distances = {
        'mobil': dist,
        'motor': int(dist * 0.9),        # Motor lebih cepat dari jalan kaki
        'jalan_kaki': int(dist * 3.5)    # Jalan kaki jauh lebih lambat
    }
    city_map.add_edge(src, dst, distances)

# Interaksi pengguna
print("======== PETA KOTA JAWA ========")
print("Daftar Kota:", ", ".join(cities))
start = input("Masukkan kota asal: ")
end = input("Masukkan kota tujuan: ")
mode = input("Pilih moda transportasi (mobil/motor/jalan_kaki): ").lower()

# Validasi input dan mulai simulasi
if start in cities and end in cities and mode in ['mobil', 'motor', 'jalan_kaki']:
    speed = {'mobil': 60, 'motor': 50, 'jalan_kaki': 5}[mode]  # Kecepatan rata-rata (km/jam)
    
    # Menghitung jalur tercepat
    path, cost = city_map.dijkstra(mode, start, end)
    time = cost / speed

    print(f"\nJalur Tercepat ({mode.capitalize()}):")
    print(" -> ".join(path))
    print(f"Total Jarak: {cost} km")
    print(f"Estimasi Waktu: {time:.2f} jam\n")

    # Menjalankan TSP untuk rute keliling semua kota
    tsp_path, tsp_cost = city_map.tsp_brute_force(mode)
    tsp_time = tsp_cost / speed

    print(f"\nRute TSP Terbaik ({mode.capitalize()}):")
    print(" -> ".join(tsp_path))
    print(f"Total Jarak: {tsp_cost} km")
    print(f"Estimasi Waktu: {tsp_time:.2f} jam\n")

    # Menggambar graf kota dengan jalur yang dihasilkan
    draw_city_graph(city_map, mode, tsp_path=tsp_path, dijkstra_path=path)
else:
    print("Input tidak valid! Pastikan nama kota dan moda transportasi sesuai.\n")
