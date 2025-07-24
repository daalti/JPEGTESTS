import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using iw.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:iw.obj=6f8307c8767df01bdf694c3118d9549bf8f46729c411ffd9d46913a5d4ab36f6
    +test_classification:System
    +name: test_pcl5_hpgl_cfgstat_iw
    +test:
        +title: test_pcl5_hpgl_cfgstat_iw
        +guid:ee9cc543-02d5-4467-981a-e394a13b031d
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_cfgstat_iw(setup_teardown, printjob, outputsaver):
    printjob.print_verify('6f8307c8767df01bdf694c3118d9549bf8f46729c411ffd9d46913a5d4ab36f6', timeout=600)
    outputsaver.save_output()
