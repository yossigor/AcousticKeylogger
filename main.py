import asyncio
import os
import shutil
from AcousticKeylogger import AcousticKeylogger 


async def time_stretch_over_accuracy():
    results = []
    for i,time_stretch_factor in enumerate([0.9,0.95,1,1.05,1.1,1.15]):
        config = {
            'dispatcher_threshold':80,
            'dispatcher_min_interval':int(14000 / time_stretch_factor),
            'dispatcher_window_size': 100,
            'dispatcher_step_size': 1,
            'dispatcher_persistence': True,
            'time_stretch': time_stretch_factor
        }
        acoustic_keylogger = AcousticKeylogger(config)
        output_dir = "temp_{}".format(i)
        target_output_dir = "temp_target_{}".format(i)
        model_name = "model_{}".format(i)
        os.makedirs(output_dir)
        os.makedirs(target_output_dir)
        await acoustic_keylogger.sound_preprocess("../samples/k260_train_test_accuracy",
        output_dir)
        await acoustic_keylogger.sound_preprocess("../samples/k260_target",
        target_output_dir)
        await acoustic_keylogger.write_model_to_disk(output_dir,model_name)
        truth = ['o','n','e','_','r','i','n','g','_','t','o','_','r','u','l','e','_'
            ,'t','h','e','m','_','a','l','l','_','o','n','e','_','r','i','n','g','_','t','o','_'
            ,'f','i','n','d','_','t','h','e','m','_','o','n','e','_','r','i','n','g','_','t','o','_'
            ,'b','r','i','n','g','_','t','h','e','m','_','a','l','l','_','a','n','d','_','i','n','_'
            ,'t','h','e','_','d','a','r','k','n','e','s','s','_','b','i','n','d','_','t','h','e','m']
        top_n = 5
        target_file = os.path.join(target_output_dir,'target_3.wav')
        accuracy = await acoustic_keylogger.classify_and_check_accuracy(model_name,target_file,truth,top_n)
        results.append((time_stretch_factor,accuracy))
        shutil.rmtree(output_dir)
        shutil.rmtree(target_output_dir)
        os.unlink(model_name)
    print(results)

async def band_pass_over_accuracy():
    results = []
    band_pass_width = 400
    for i,band_pass_center in enumerate(range(12900,20000,400)):
        config = {
            'dispatcher_threshold':80,
            'dispatcher_min_interval':int(14000),
            'dispatcher_window_size': 100,
            'dispatcher_step_size': 1,
            'dispatcher_persistence': True,
            #'time_stretch': time_stretch_factor
            'band_pass_width': band_pass_width,
            'band_pass_center': band_pass_center,
        }
        acoustic_keylogger = AcousticKeylogger(config)
        output_dir = "temp_{}".format(i)
        target_output_dir = "temp_target_{}".format(i)
        model_name = "model_{}".format(i)
        os.makedirs(output_dir)
        os.makedirs(target_output_dir)
        await acoustic_keylogger.sound_preprocess("../samples/k260_train_test_accuracy",
        output_dir)
        await acoustic_keylogger.sound_preprocess("../samples/k260_target",
        target_output_dir)
        await acoustic_keylogger.write_model_to_disk(output_dir,model_name)
        truth = ['o','n','e','_','r','i','n','g','_','t','o','_','r','u','l','e','_'
            ,'t','h','e','m','_','a','l','l','_','o','n','e','_','r','i','n','g','_','t','o','_'
            ,'f','i','n','d','_','t','h','e','m','_','o','n','e','_','r','i','n','g','_','t','o','_'
            ,'b','r','i','n','g','_','t','h','e','m','_','a','l','l','_','a','n','d','_','i','n','_'
            ,'t','h','e','_','d','a','r','k','n','e','s','s','_','b','i','n','d','_','t','h','e','m']
        top_n = 5
        target_file = os.path.join(target_output_dir,'target_3.wav')
        accuracy = await acoustic_keylogger.classify_and_check_accuracy(model_name,target_file,truth,top_n)
        results.append((band_pass_center,accuracy))
        shutil.rmtree(output_dir)
        shutil.rmtree(target_output_dir)
        os.unlink(model_name)
    print(results)


async def main():
    await band_pass_over_accuracy()

    

asyncio.run(main())
