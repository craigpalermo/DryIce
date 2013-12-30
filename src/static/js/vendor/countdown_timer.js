/*
 This variable is used to keep track of the timers that are still running.
 * It stores the ID's of the running times. This is used to prevent
 * multiple timers from being initialized on the same html field at once.
 */
var runningTimerIds = new Array();

/**
 This function is used to start the count-down timers on the page. (Both
 the one at the top, and the one that appears in the lower right corner).
 You need to pass in the end time for the timer as a Date object in
 local time. If there is more than one hour remaining, the time displayed
 on the page is in HH:MM:SS format, and if there is less that one hour
 remaining the format is MM:SS.
 * @param endTime
 * Date object with the timer end time
 */

function startCountdown(endTime, id) {

    /*
     * Check to see if the ID is contained in the runningTimerIds
     * array. If it is, then we return out of this method to prevent
     * another timer from being made.
     */
    if(runningTimerIds.indexOf(id) > -1){
        return;
    }

    /**
     * This function is responsible for modifying the countdown timer.
     * When time is up, it raises a dialog box.
     */
    function countdownTimer() {

        // Get the current time.
        var currentTime = new Date();

        /*
         * If the time is up; (the currentTime is greater than or equal
         * to the
         * endingTime), then we want to stop the timer from updating by
         * returning.
         */
        if (currentTime >= endTime) {
            // Set the timer to 00:00
            $('#' + id + '_timeRemaining').html('00:00');

            /*
             * Since this timer is expired, it will be removed from the
             * page; so we remove its id from the runningTimerIds array.
             */
            runningTimerIds.splice($.inArray(id, runningTimerIds), 1);

            // Stop updating the timer by returning
            return;
        }

        /*
         * Calculate the milliseconds remaining between the current time
         * and the ending time.
         */
        var msecRemaining = endTime - currentTime;

        /*
         * Calculate the seconds, minutes, and hours remaining that will be
         * displayed on the timer. These values do NOT represent the
         * absolute
         * seconds, minutes, and hours remaining. The secondsRemaining and
         * minutesRemaining are restricted values that can only range
         * from 0~59
         * (which is why the modulus is present). The hours field is
         * unbounded.
         */
        var secondsRemainingOnTimer =
                                    Math.floor(msecRemaining / 1000) % 60;
        var minutesRemainingOnTimer =
                                    Math.floor(msecRemaining / 60000) % 60;
        var hoursRemainingOnTimer = Math.floor(msecRemaining / 3600000);

        /*
         * Properly format the remaining time by adding a leading zero to
         * the number if it is a single digit. I.e. [03:01:09]
         */
        if (hoursRemainingOnTimer > 0 && hoursRemainingOnTimer < 10) {
            hoursRemainingOnTimer =
                ("0" + hoursRemainingOnTimer).slice(-2);
        }

        minutesRemainingOnTimer =
            ("0" + minutesRemainingOnTimer).slice(-2);
        secondsRemainingOnTimer =
            ("0" + secondsRemainingOnTimer).slice(-2);

        // Declare the string that will be displayed on the timer
        var formattedTimeString = '';

        /*
         * Create the timer string (formattedTimeString) in the format
         * HH:MM:SS.
         * Omit the hours segment if the timer ends in less than 1 hour.
         */
        if (hoursRemainingOnTimer == 0) {
            formattedTimeString = minutesRemainingOnTimer + ':'
                    + secondsRemainingOnTimer
        } else {
            formattedTimeString = hoursRemainingOnTimer + ':'
                    + minutesRemainingOnTimer + ':' +
                    secondsRemainingOnTimer;
        }

        // Display the formattedTimeString on the page.
        $('#' + id + '_timeRemaining').html(formattedTimeString);

        // Re-evaluate the time 60 times per second
        setTimeout(countdownTimer, 16.6667);
    }

    // Add this id to the list of running timers
    runningTimerIds.push(id);

    // Start the countdown timer
    countdownTimer();
};
