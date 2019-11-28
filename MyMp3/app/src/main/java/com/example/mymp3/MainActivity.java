package com.example.mymp3;

import android.content.Context;
import android.media.AudioManager;
import android.media.MediaPlayer;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.os.Message;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    private TextView title;
    private ImageView thumbnail;
    private Button play;
    private Button next;
    private Button prev;

    private MediaPlayer mediaPlayer;
    private int[] songID = new int[]{R.raw.nam, R.raw._2002, R.raw.speechless, R.raw.punch, R.raw.workaholic};
    private String[] songTitle = new String[]{"남이 될 수 있을까", "2002", "Speechless", "가끔 이러다", "워커홀릭"};
    private int[] songThumbnail = new int[]{R.drawable.nam, R.drawable._2002, R.drawable.speechless, R.drawable.punch, R.drawable.workaholic};
    private boolean isPlay = true;
    private int songIdx = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        setTheme(R.style.Theme_AppCompat_NoActionBar);
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        title = findViewById(R.id.Title);
        thumbnail = findViewById(R.id.Thumbnail);
        play = findViewById(R.id.Play);
        prev = findViewById(R.id.Prev);
        next = findViewById(R.id.Next);

        Context context = getApplicationContext();

        mediaPlayer = MediaPlayer.create(MainActivity.this, songID[songIdx]);
        mediaPlayer.start();
        update();

        play.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (isPlay) {
                    isPlay = false;
                    mediaPlayer.pause();
                } else {
                    isPlay = true;
                    mediaPlayer.start();
                }
                update();
            }
        });

        next.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                nextSong();
            }
        });

        prev.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                prevSong();
            }
        });

        // test 용
        title.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                volUp();
            }
        });

        thumbnail.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                volDown();
            }
        });

        Handler mHandler = new Handler(Looper.getMainLooper()) {
            @Override
            public void handleMessage(Message inputMessage) {
                switch(inputMessage.what) {

                    // CONNECTED == 0 / DATA == 1 / DISCONNECTED == 3
                    case 0:
                        // do something with UI
                        Log.d("connected!", "connected with server!");
                        break;

                    case 1:
                        String msg = (String) inputMessage.obj;
                        Log.d("socket", "Socket Data Receive !!");

                        if (msg.equals("r2l")){
                            prevSong();
                        }
                        else if (msg.equals("l2r")){
                            nextSong();
                        }
                        else if (msg.equals("cw")){
                            volUp();
                        }
                        else if (msg.equals("ccw")){
                            volDown();
                        }
                        break;
                }
            }
        };

        ClientSocket socket = new ClientSocket("192.168.4.5", 32990, mHandler, context);
        socket.start();
    }

   private void update() {
        if (isPlay) {
            play.setBackground(getResources().getDrawable(R.drawable.pause));
        } else {
            play.setBackground(getResources().getDrawable(R.drawable.play));
        }

        title.setText(songTitle[songIdx]);
        thumbnail.setBackground(getResources().getDrawable(songThumbnail[songIdx]));
    }

    private void volUp() {
        AudioManager am = (AudioManager) getSystemService(Context.AUDIO_SERVICE);
        int volume = am.getStreamVolume(AudioManager.STREAM_MUSIC);

        if (volume > 0) {
            am.setStreamVolume(AudioManager.STREAM_MUSIC, volume - 1, AudioManager.FLAG_PLAY_SOUND);
        }
    }

    private void volDown() {
        AudioManager am = (AudioManager) getSystemService(Context.AUDIO_SERVICE);
        int volume = am.getStreamVolume(AudioManager.STREAM_MUSIC);

        if (volume < 15) {
            am.setStreamVolume(AudioManager.STREAM_MUSIC, volume + 1, AudioManager.FLAG_PLAY_SOUND);
        }
    }

    private void nextSong(){
        if (songIdx == songID.length - 1) {
            songIdx = 0;
        } else {
            songIdx++;
        }

        if (mediaPlayer != null) {
            mediaPlayer.release();
            mediaPlayer = null;
        }

        mediaPlayer = MediaPlayer.create(MainActivity.this, songID[songIdx]);
        mediaPlayer.start();
        isPlay = true;
        update();
    }

    private void prevSong(){
        if (songIdx == 0) {
            songIdx = songID.length - 1;
        } else {
            songIdx--;
        }

        if (mediaPlayer != null) {
            mediaPlayer.release();
            mediaPlayer = null;
        }

        mediaPlayer = MediaPlayer.create(MainActivity.this, songID[songIdx]);
        mediaPlayer.start();
        isPlay = true;
        update();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        // MediaPlayer 해지
        if (mediaPlayer != null) {
            mediaPlayer.release();
            mediaPlayer = null;
        }
    }
}
