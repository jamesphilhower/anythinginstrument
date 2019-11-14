
    {
        const playingClass = 'playing',
            crashRide = document.getElementById('crash-ride'),
            hiHatTop = document.getElementById('hihat-top');

        function playSound(e){
            const keyCode = e,
                keyElement = document.querySelector(`div[data-key="${e}"]`);

            if(!keyElement) return;

            const audioElement = document.querySelector(`audio[data-key="${e}"]`);
            audioElement.currentTime = 0;
            audioElement.play();

            switch(keyCode) {
                case 69:
                case 82:
                    animateCrashOrRide();
                    break;
                case 75:
                    animateHiHatClosed();
                    break;
            }

            keyElement.classList.add(playingClass);
        };

        const removeCrashRideTransition = e => {
            if(e.propertyName !== 'transform') return;

            e.target.style.transform = 'rotate(-7.2deg) scale(1.5)';
        };

        const removeHiHatTopTransition = e => {
            if(e.propertyName !== 'top') return;

            e.target.style.top = '166px';
        };	

        const removeKeyTransition = e => {
            if(e.propertyName !== 'transform') return;

            e.target.classList.remove(playingClass)
        };

        const drumKeys = Array.from(document.querySelectorAll('.key'));

        drumKeys.forEach(key => {
            key.addEventListener('transitionend', removeKeyTransition);
        });

    }

      var i = 0;
      function nextFrame() {
        someanimation();
        i++;
        // Continue the loop in 3s
        setTimeout(nextFrame, 300);
      }
      // Start the loop
      setTimeout(nextFrame, 0);
      function someanimation(){
        fetch("{{url_for('text_feed') }}").then((response) => response.text().then(yourCallback));
      }
      function yourCallback( retrievedText ) { 
            console.log(retrievedText);
            playSound(retrievedText);
        }    