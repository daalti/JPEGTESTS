import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 40Page_sm_ct.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:40Page-sm_ct.obj=d395431afb90ac118151ca55a0cb30d489fc93a3d12f105670f33c1ab93587a2
    +test_classification:System
    +name: test_pcl5_highvalue_40page_sm_ct
    +test:
        +title: test_pcl5_highvalue_40page_sm_ct
        +guid:c179a092-b146-4cf2-9704-7010dfd8c5c7
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_40page_sm_ct(setup_teardown, printjob, outputsaver):
    printjob.print_verify('d395431afb90ac118151ca55a0cb30d489fc93a3d12f105670f33c1ab93587a2', timeout=600)
    outputsaver.save_output()
