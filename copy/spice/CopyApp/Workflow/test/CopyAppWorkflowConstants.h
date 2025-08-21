#ifndef COPY_APP_WORKFLOW_CONSTANTS_H
#define COPY_APP_WORKFLOW_CONSTANTS_H

#include <QString>

namespace CopyAppState {
    // Define string constants for each state
    const QString GET_CONFIGURATIONS = "GET_CONFIGURATIONS";
    const QString IDLE = "IDLE";
    const QString COPY_LANDING = "COPY_LANDING";
    const QString EXECUTE_ONE_TOUCH_JOB_AND_EXIT = "EXECUTE_ONE_TOUCH_JOB_AND_EXIT";
    const QString CONSTRAINED = "CONSTRAINED";
    const QString PREVIEW = "PREVIEW";
    const QString PREVIEW_IN_PROGRESS = "PREVIEW_IN_PROGRESS";
    const QString CANCELLED = "CANCELLED";
    const QString PREPARE_TO_PREVIEW = "PREPARE_TO_PREVIEW";
    const QString PREVIEW_READY = "PREVIEW_READY";
}

#endif // COPY_APP_WORKFLOW_CONSTANTS_H