#include "CopyInitView.h"

#include <QMetaObject>

#include "CopyAppController.h"
#include "CoreActivityFilter.h"
namespace dune { namespace copy { namespace spice {

CopyInitView::CopyInitView(SpiceView::ViewPriority priority, ISpiceController *controller, QObject *parent)
    : SpiceView(priority, controller, parent)
{
    operation_ = {
        new KeyOperation(new HardKey("COPYSTART", KeyMappingType::eCOPY, KeyAction::eCLICK, 1000), "startCopy"),
        new KeyOperation(new HardKey("COPYDECREMENT", KeyMappingType::eCOPYDCR, KeyAction::eCLICK, 1000),
                         "decrementCopies"),
        new KeyOperation(new HardKey("COPYINCREMENT", KeyMappingType::eCOPYINCR, KeyAction::eCLICK, 1000),
                         "incrementCopies")};

    CopyAppController *copyAppctrl = static_cast<CopyAppController *>(controller_);
    auto               copies = copyAppctrl->getDefaultCopies();
    DUNE_UNUSED(copies);
    // applicationEngine_->getLedManager()->setLed(copiesLed);
}
void CopyInitView::onActive()
{
    IKeyHandler *keyHandler = controller_->getApplicationEngine()->getKeyHandler();
    keyHandler->disableKey(KeyMappingType::eCANCEL);
}
}}}  // namespace dune::copy::spice
