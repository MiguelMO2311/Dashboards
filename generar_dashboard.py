import os
import shutil

# Solicitar datos al usuario
html_filename = input("Introduce el nombre del archivo HTML (sin extensión): ") + ".html"
num_sheets = int(input("Introduce el número de hojas adicionales (sin contar 'Hoja Principal'): "))

# Crear lista de hojas con "Hoja Principal"
sheets = ["Hoja Principal"]
for i in range(num_sheets):
    sheet_name = input(f"Introduce el nombre de la hoja {i+1}: ")
    sheets.append(sheet_name)

# Plantilla HTML con estructura dinámica
html_template = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html_filename}</title>
    <link href="tailwind.css" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.4.0/jspdf.umd.min.js"></script>
    <script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            display: flex;
            flex-direction: column;
            height: 100vh;
            background-color: #EFF2F7;
            font-family: 'Inter', sans-serif;
            color: #333;
        }}
        .header {{
            background: linear-gradient(135deg, #3B82F6 0%, #1E293B 100%);
            padding: 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            width: 100%;
            position: fixed;
            top: 0;
            left: 0;
        }}
        .sidebar {{
            background: #2E3A46;
            width: 80px;
            height: calc(100vh - 80px);
            position: fixed;
            left: 0;
            top: 80px;
            padding: 10px;
            transition: width 0.3s ease;
        }}
        .sidebar.collapsed {{
            width: 20px;
        }}
        .content {{
            margin-left: 80px;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 20px;
            height: calc(100vh - 160px);
        }}
        .collapsed + .content {{
            margin-left: 20px;
        }}
        .footer {{
            background: linear-gradient(135deg, #3B82F6 0%, #1E293B 100%);
            padding: 20px;
            width: 100%;
            position: fixed;
            bottom: 0;
            left: 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .toggle-btn {{
            background-color: #444;
            color: white;
            padding: 5px 10px;
            border: none;
            cursor: pointer;
        }}
        .pagination-btn {{
            background-color: #ffffff;
            color: #333;
            padding: 10px;
            border-radius: 5px;
            cursor: pointer;
            border: none;
        }}
        .sheet {{
            display: none;
        }}
        .sheet.active {{
            display: block;
        }}
        .dark-mode {{
            background-color: #10151D;
            color: white;
        }}
    </style>
</head>
<body>

    <header class="header">
        <img src="logo.png" alt="Logo Empresa" width="50">
        <h1 id="page-title" class="text-3xl font-bold text-white" contenteditable="true">Hoja Principal</h1>
        <button onclick="toggleDarkMode()" class="bg-gray-800 hover:bg-gray-600 text-white px-4 py-2 rounded">Modo Oscuro/Claro</button>
        <button onclick="publicarDashboard()" class="bg-green-500 hover:bg-green-700 text-white px-4 py-2 rounded">Publicar</button>
        <button onclick="generarPDF()" class="bg-purple-500 hover:bg-purple-700 text-white px-4 py-2 rounded">Generar PDF</button>
        <button onclick="capturarDashboard()" class="bg-blue-500 hover:bg-blue-700 text-white px-4 py-2 rounded">Capturar PNG</button>
    </header>

    <div class="sidebar" id="sidebar">
        <button onclick="toggleSidebar()" class="toggle-btn">⇆</button>
        <p class="text-white"> Añadir Filtros aquí</p>
    </div>

    <div class="content">
        {sheet_sections}
    </div>

    <footer class="footer">
        <p class="text-white">© 2025 - Empresa Dashboard</p>
        {pagination_buttons}
    </footer>

    <script>
        function toggleSidebar() {{
            document.getElementById('sidebar').classList.toggle('collapsed');
            document.querySelector('.content').classList.toggle('collapsed');
        }}

        function toggleDarkMode() {{
            document.body.classList.toggle('dark-mode');
        }}

        function publicarDashboard() {{
            let url = prompt("Introduce la URL de publicación:");
            if (url && url.startsWith("http")) {{
                alert("Publicando en " + url);
            }} else {{
                alert("No se ingresó una URL válida.");
            }}
        }}

        function generarPDF() {{
            document.querySelectorAll('.hide-on-export').forEach(el => el.style.display = 'none');
            window.print();
            document.querySelectorAll('.hide-on-export').forEach(el => el.style.display = 'block');
        }}

        function showSheet(sheetId, sheetTitle) {{
            document.querySelectorAll('.sheet').forEach(sheet => sheet.classList.remove('active'));
            document.getElementById(sheetId).classList.add('active');
            document.getElementById('page-title').innerText = sheetTitle;
        }}

        function capturarDashboard() {{
            html2canvas(document.body).then(canvas => {{
                let imgData = canvas.toDataURL("image/png");
                let link = document.createElement("a");
                link.href = imgData;
                link.download = "dashboard.png";
                link.click();
            }});
        }}
    </script>

</body>
</html>
"""

# Generar secciones de hojas y botones de paginación
sheet_sections = "\n".join([f'<div id="sheet{i}" class="sheet{" active" if i == 0 else ""}"><h2 class="sheet-title" contenteditable="true">{name}</h2></div>' for i, name in enumerate(sheets)])
pagination_buttons = "\n".join([f'<button class="pagination-btn" onclick="showSheet(\'sheet{i}\', \'{name}\')">{name}</button>' for i, name in enumerate(sheets)])

# Reemplazar en la plantilla
html_content = html_template.format(html_filename=html_filename, sheet_sections=sheet_sections, pagination_buttons=pagination_buttons)

# Guardar el archivo HTML
with open(html_filename, "w", encoding="utf-8") as f:
    f.write(html_content)

# Script para mover la imagen descargada
img_source = os.path.expanduser("~/Downloads/dashboard.png")
img_dest = "C:\\Users\\Usuario\\Desktop\\Miguel\\IBM SkillsBuild\\PowerBI\\Dashboards\\dashboard.png"

if os.path.exists(img_source):
    shutil.move(img_source, img_dest)
    print(f"✅ Imagen movida a: {img_dest}")
else:
    print("⚠️ No se encontró la imagen. Asegúrate de haberla descargado primero.")

print(f"Archivo HTML '{html_filename}' generado correctamente.")
