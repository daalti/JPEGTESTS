import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 89Page_cttfdes.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:1500
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:89Page-cttfdes.obj=5eb1c4396a9b4ad3aed87c28f8bcfea0e9a51a561c6a4b518e9f265980f48c02
    +test_classification:System
    +name: test_pcl5_highvalue_89page_cttfdes
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_89page_cttfdes
        +guid:1adb2a59-266f-4b0d-80df-63557284d022
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_89page_cttfdes(setup_teardown, printjob, outputsaver):
    printjob.print_verify('5eb1c4396a9b4ad3aed87c28f8bcfea0e9a51a561c6a4b518e9f265980f48c02', timeout=1500)
    outputsaver.save_output()
