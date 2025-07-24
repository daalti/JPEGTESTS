import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 basicfunctionality using 14Page_udssval.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:14Page-udssval.obj=380b283d10af04c5211e83373bd2a8bc1e598bc5906d5d0bcf625b6d0737a124
    +test_classification:System
    +name: test_pcl5_basicfunctionality_14page_udssval
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_basicfunctionality_14page_udssval
        +guid:f0e26fc2-b765-4a21-9b07-279006467b94
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_basicfunctionality_14page_udssval(setup_teardown, printjob, outputsaver):
    printjob.print_verify('380b283d10af04c5211e83373bd2a8bc1e598bc5906d5d0bcf625b6d0737a124', timeout=300)
    outputsaver.save_output()
