import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 allocidcoverage using configure.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:configure.pcl=ee655ab156898d558a4b886fb6153f6f28682b59b90e26a457fbbd4e8e3704b1
    +test_classification:System
    +name: test_pcl5_allocidcoverage_configure
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_allocidcoverage_configure
        +guid:5806f8d6-99f8-487a-926b-f71ea2c197fb
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_allocidcoverage_configure(setup_teardown, printjob, outputsaver):
    printjob.print_verify('ee655ab156898d558a4b886fb6153f6f28682b59b90e26a457fbbd4e8e3704b1', timeout=600)
    outputsaver.save_output()
