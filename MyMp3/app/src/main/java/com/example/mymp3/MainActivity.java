package com.example.mymp3;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.Manifest;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.media.AudioManager;
import android.media.MediaPlayer;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;
import android.view.accessibility.AccessibilityManager;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.UUID;

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
