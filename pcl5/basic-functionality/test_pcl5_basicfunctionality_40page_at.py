import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 basicfunctionality using 40Page_at.obj
    +test_tier: 1
    +is_manual:False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:240
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:40Page-at.obj=497815f205db367569544a23af955e93d9519102048b26f726ad92a84dbc27aa
    +test_classification:System
    +name: test_pcl5_basicfunctionality_40page_at
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_basicfunctionality_40page_at
        +guid:afe59473-d590-4d16-85fb-ece5c3cf4133
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_basicfunctionality_40page_at(setup_teardown, printjob, outputsaver):
    printjob.print_verify('497815f205db367569544a23af955e93d9519102048b26f726ad92a84dbc27aa',timeout=240)
    outputsaver.save_output()
