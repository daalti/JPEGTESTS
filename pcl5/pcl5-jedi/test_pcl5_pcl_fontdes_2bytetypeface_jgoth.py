import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using jgoth.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:jgoth.obj=e9bf371a76d15687e1e7f3b621e0380811d23cb8291c7bb386b9f3687909843c
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_jgoth
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_jgoth
        +guid:a34f3537-0b07-4496-ba38-8a70b99ed39c
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_jgoth(setup_teardown, printjob, outputsaver):
    printjob.print_verify('e9bf371a76d15687e1e7f3b621e0380811d23cb8291c7bb386b9f3687909843c', timeout=600)
    outputsaver.save_output()
