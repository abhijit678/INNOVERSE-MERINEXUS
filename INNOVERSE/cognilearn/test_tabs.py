import app

try:
    print("Testing tab 1...")
    app.render_tab_1()
    print("Tab 1 OK")
    
    print("Testing tab 2...")
    app.render_tab_2()
    print("Tab 2 OK")
    
    print("Testing tab 3...")
    app.render_tab_3()
    print("Tab 3 OK")
except Exception as e:
    import traceback
    traceback.print_exc()
