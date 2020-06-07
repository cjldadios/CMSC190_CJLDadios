\version "2.18.2"

% Lilypond template

\header {
    title = "My Score"
    composer = " "
    tagline = ##f
}

\language "english"

#(define harald '(
         (bassdrum        default   #f           -3) 
         (snare           default   #f            1)
         (sidestick       cross     #f            1)
         (himidtom        default   #f            3)
         (lowtom          default   #f           -1)
         (hihat           cross     #f            5)
         (openhihat       cross     "open"        5)
         (pedalhihat      cross     #f           -5)
         (crashcymbal     cross     #f            6)
         (ridecymbal      cross     #f            4)
         (ridebell        diamond   #f            4)))
         % The number is "semitones away from the middle staff (0)"

\drums {
    \set DrumStaff.drumStyleTable = #(alist->hash-table harald)
    \stemUp
    \override Beam #'damping = #+inf.0 % set beams horizontal
    \time 4/4
    \tempo 4 = 120
    <bd cymc>8 <ss hh>8 <sn tommh>8 hhp8 <bd cymr>8 cymr8 <sn cymr>8 tommh16 toml16 
}


up = \drummode {
  crashcymbal4 hihat8 halfopenhihat hh hh rb hho
}
down = \drummode {
  bassdrum4 snare8 bd r bd sn4
}

\new DrumStaff <<
  \set DrumStaff.drumStyleTable = #(alist->hash-table harald)
  \new DrumVoice { \voiceOne \up }
  \new DrumVoice { \voiceTwo \down }
>>

% bassdrum bd
% snare sn
% sidestick ss
% himidtom tommh
% lowtom toml
% closedhihat hhc
% openhihat hho
% pedalhihat hhp
% crashcymbal cymc
% ridecymbal cymr
% ridebell rb


% Harald Huyssen notation
% Crash: first ledger line above 
% Ride: above the top line
% Hihat: through the top staff
% Rack tom: top space
% Floor tom: second space from below
