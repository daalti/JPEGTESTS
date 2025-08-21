#include "CopyStartView.h"

#include <QMetaObject>

#include "CopyAppController.h"
#include "IApplicationEngine.h"

namespace dune { namespace copy { namespace spice {
using namespace dune::spice::core;

CopyStartView::CopyStartView(SpiceView::ViewPriority priority, ISpiceController *controller, QObject *parent)
    : SpiceView(priority, controller, parent)
{
    operation_ = {
        new KeyOperation(new HardKey("COPYCANCEL", KeyMappingType::eCANCEL, KeyAction::eCLICK, 1000), "cancelCopy")};
}

void CopyStartView::onActive()
{
    IKeyHandler *keyHandler = controller_->getApplicationEngine()->getKeyHandler();
    keyHandler->disableKey(KeyMappingType::eCOPY);
    keyHandler->enableKey(KeyMappingType::eCANCEL);
}

}}}  // namespace dune::copy::spice
