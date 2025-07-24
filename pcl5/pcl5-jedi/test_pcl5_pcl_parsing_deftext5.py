import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using deftext5.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:deftext5.obj=ad146238a67542d39e946b1aace1753061e5333f8a28dee3a7965bc193413587
    +test_classification:System
    +name: test_pcl5_pcl_parsing_deftext5
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_pcl_parsing_deftext5
        +guid:82bf2090-ffc5-4920-9d93-8e52f34715dd
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_parsing_deftext5(setup_teardown, printjob, outputsaver):
    printjob.print_verify('ad146238a67542d39e946b1aace1753061e5333f8a28dee3a7965bc193413587', timeout=600)
    outputsaver.save_output()
