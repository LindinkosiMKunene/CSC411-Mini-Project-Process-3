
def render_client_page(title, header_bg, role_name, agency_name, port_num, main_script):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 0; padding: 0;
            background-color: #f8fafc;
            color: #0f172a;
        }}
        header {{
            background-color: {header_bg};
            color: white;
            padding: 20px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }}
        header h1 {{ margin: 0; font-size: 1.4rem; }}
        .badge {{
            background: rgba(255, 255, 255, 0.2);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: bold;
        }}
        main {{
            max-width: 900px;
            margin: 30px auto;
            padding: 0 20px;
        }}
        .card {{
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }}
        .card h2 {{
            margin-top: 0;
            color: {header_bg};
            border-bottom: 2px solid #f1f5f9;
            padding-bottom: 10px;
        }}
        .form-group {{ margin-bottom: 16px; }}
        label {{ display: block; font-weight: 600; margin-bottom: 6px; font-size: 0.9rem; }}
        input, select, textarea {{
            width: 100%;
            padding: 10px 12px;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            box-sizing: border-box;
            font-size: 0.95rem;
        }}
        button {{
            width: 100%;
            background-color: {header_bg};
            color: white;
            border: none;
            padding: 12px;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
            transition: opacity 0.2s;
        }}
        button:hover {{ opacity: 0.9; }}
        pre {{
            background: #0f172a;
            color: #38bdf8;
            padding: 16px;
            border-radius: 6px;
            overflow-x: auto;
            font-size: 0.85rem;
        }}
    </style>
</head>
<body>
    <header>
        <h1>🇸🇿 {title}</h1>
        <div class="badge">Port {port_num} | Agency: {agency_name}</div>
    </header>
    <main>
        {main_script}
    </main>
</body>
</html>'''
