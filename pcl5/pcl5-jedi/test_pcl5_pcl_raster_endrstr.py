import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using endrstr.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:endrstr.obj=47773b25eef6afc0f3880128aaf22ed3c5354bcee3cf08a2c2053ab7128624f3
    +test_classification:System
    +name: test_pcl5_pcl_raster_endrstr
    +test:
        +title: test_pcl5_pcl_raster_endrstr
        +guid:9d584a30-921b-47d1-b056-52c2df755841
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_raster_endrstr(setup_teardown, printjob, outputsaver):
    printjob.print_verify('47773b25eef6afc0f3880128aaf22ed3c5354bcee3cf08a2c2053ab7128624f3', timeout=600)
    outputsaver.save_output()
