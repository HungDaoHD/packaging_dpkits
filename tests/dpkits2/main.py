from dpkits2.manager import Manager



mgr = Manager(folder_name='tests\\dpkits2\\DataToRun', file_name='VN9999 - Project Name.xlsx')
mgr.run()

# mgr.data_bundle.metadata.save_json('tests\\dpkits2\\metadata.json')
    
mgr.data_bundle.metadata = mgr.data_bundle.metadata.from_json_file('tests\\dpkits2\\metadata.json')







print('>>> Finish Tasks')





