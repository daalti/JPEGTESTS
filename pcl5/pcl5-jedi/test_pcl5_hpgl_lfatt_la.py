import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using la.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:la.obj=f5eb8d265978552e0815d43b6f5b647698cfc02d0dc6a53b4e5c16711e454452
    +test_classification:System
    +name: test_pcl5_hpgl_lfatt_la
    +test:
        +title: test_pcl5_hpgl_lfatt_la
        +guid:fc3fc3b7-fde4-425f-bca0-981ad9e4264d
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_lfatt_la(setup_teardown, printjob, outputsaver):
    printjob.print_verify('f5eb8d265978552e0815d43b6f5b647698cfc02d0dc6a53b4e5c16711e454452', timeout=600)
    outputsaver.save_output()
