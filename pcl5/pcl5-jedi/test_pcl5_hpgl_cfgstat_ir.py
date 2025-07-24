import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using ir.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ir.obj=229f31ce7e9aed8a7d9ff19e5b7fe3c2b377859786c65abfe97ddb64629926d6
    +test_classification:System
    +name: test_pcl5_hpgl_cfgstat_ir
    +test:
        +title: test_pcl5_hpgl_cfgstat_ir
        +guid:a82f2e90-509c-4628-b9c2-cf530e12d0b0
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_cfgstat_ir(setup_teardown, printjob, outputsaver):
    printjob.print_verify('229f31ce7e9aed8a7d9ff19e5b7fe3c2b377859786c65abfe97ddb64629926d6', timeout=600)
    outputsaver.save_output()
