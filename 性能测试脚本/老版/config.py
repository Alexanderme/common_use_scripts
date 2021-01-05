class Config:
    """
    需要用户不用镜像不同服务器的时候 基本参数配置
    """
    # 测试服务器内存大小 M
    # 测试服务器显存大小 M
    mem_total = 31947
    nvidia_total = 5942
    cpu_cores = 6

    sleep_time = 300
    fps_times = 5000

    # 保存结果文件夹
    base_dir = "/ljx/res"
    # 挂载目录文件夹
    main_dir = "/ljx"
    con_dir = "/ljx"

    roi_pol = "POLYGON((0.07 0.0775,0.08 0.88,0.9 0.8575,0.9 0.05))"
    roi_line_pol = "POLYGON((0.07 0.0775,0.08 0.88,0.9 0.8575,0.9 0.05))|LINESTRING(0.2 0.4475,0.8 0.445)"
    roi_poi_line_pol = "POLYGON((0.07 0.0775,0.08 0.88,0.9 0.8575,0.9 0.05))|LINESTRING(0.2 0.4475,0.8 0.445)|POINT(0.5 0.3075)"
    
    hk_plate_path = "export LD_LIBRARY_PATH=/usr/local/cuda-9.0/lib64/:$LD_LIBRARY_PATH" 
    run_methods_6 = "%s;/usr/local/ev_sdk/bin/test -f 1 -l /usr/local/ev_sdk/bin/license.txt -i %s/1.jpg" % (hk_plate_path, main_dir)
    
    xiaofang_path = "export LD_LIBRARY_PATH=/opt/intel/computer_vision_sdk_2018.5.455/deployment_tools/inference_engine/external/mkltiny_lnx/lib/:/opt/intel/computer_vision_sdk_2018.5.455/deployment_tools/inference_engine/lib/ubuntu_16.04/intel64/:/opt/intel/computer_vision_sdk_2018.5.455/openvx/lib/:$LD_LIBRARY_PATH"
    run_methods_7 = "%s;./test -f 1 -i %s/1.jpg " % (xiaofang_path, main_dir)

    keliu_path = "export LD_LIBRARY_PATH=/opt/intel/computer_vision_sdk_2018.5.455/deployment_tools/inference_engine/lib/ubuntu_16.04/intel64/:/opt/intel/computer_vision_sdk_2018.5.445/deployment_tools/inference_engine/external/mkltiny_lnx/lib/:$LD_LIBRARY_PATH"
    run_methods_8 = "%s;/usr/local/ev_sdk/bin/test -f 1 -l /usr/local/ev_sdk/bin/license.txt -i %s/1.jpg -a '%s'" % (keliu_path, main_dir, roi_poi_line_pol)
    

    ev_path = "export LD_LIBRARY_PATH=/usr/local/cuda-10.0/lib64:/usr/local/nvidia/lib:/usr/local/nvidia/lib64"

    """ 算法2.0的配置"""
    # 默认分析全部
    run_methods_1 = "%s;/usr/local/ev_sdk/bin/test -f 1 -l /usr/local/ev_sdk/bin/license.txt -i %s/1.jpg" % (
        ev_path, main_dir)
    # 默认分析框
    run_methods_2 = "%s;/usr/local/ev_sdk/bin/test -f 1 -l /usr/local/ev_sdk/bin/license.txt -i %s/1.jpg  -a '%s'" % (
        ev_path, main_dir, roi_pol)
    # 默认分析线框
    run_methods_3 = "%s;/usr/local/ev_sdk/bin/test -f 1 -l /usr/local/ev_sdk/bin/license.txt -i %s/1.jpg  -a '%s'" % (
        ev_path, main_dir, roi_line_pol)

    # 默认分析点线框
    run_methods_4 = "%s;/usr/local/ev_sdk/bin/test -f 1 -l /usr/local/ev_sdk/bin/license.txt -i %s/1.jpg  -a '%s'" % (
        ev_path, main_dir, roi_poi_line_pol)

    """ 算法3.0的配置"""
    # 默认分析全部
    run_methods_5 = "%s;/usr/local/ev_sdk/bin/test-ji-api -f 1 -l /usr/local/ev_sdk/authorization/license.txt -i %s/1.jpg " % (
        ev_path, main_dir)

    # 算法报警图片名称


    image_names=[("镜像地址", run_methods_2)]
