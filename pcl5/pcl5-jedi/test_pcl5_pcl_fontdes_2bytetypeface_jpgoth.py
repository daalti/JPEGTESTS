import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using jpgoth.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:jpgoth.obj=9d94926deb05a308447141505fd78b6e544908bcb856d0b0689131636e40a584
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_jpgoth
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_jpgoth
        +guid:9dd848d6-e6c1-491b-af25-7857993c175f
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_jpgoth(setup_teardown, printjob, outputsaver):
    printjob.print_verify('9d94926deb05a308447141505fd78b6e544908bcb856d0b0689131636e40a584', timeout=600)
    outputsaver.save_output()
