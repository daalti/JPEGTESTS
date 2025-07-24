import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using di.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:di.obj=64eafdc3c162a7f2a53b3e43e129b0a3d42e186605d4d91526beb03c61709be7
    +test_classification:System
    +name: test_pcl5_hpgl_char_di
    +test:
        +title: test_pcl5_hpgl_char_di
        +guid:0068d2e5-9082-4437-9a3b-c6d570a6c7ad
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_di(setup_teardown, printjob, outputsaver):
    printjob.print_verify('64eafdc3c162a7f2a53b3e43e129b0a3d42e186605d4d91526beb03c61709be7', timeout=600)
    outputsaver.save_output()
