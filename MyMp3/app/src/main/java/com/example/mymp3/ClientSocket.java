package com.example.mymp3;

import android.content.Context;
import android.util.Log;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.ObjectOutputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.text.SimpleDateFormat;
import java.util.Date;
import android.os.Handler;
import android.os.Message;

public class ClientSocket extends Thread{

    // Socket 관련 변수들
    private Socket socket;
    private String addr = "";
    private int port;
    private Handler handler = null;
    // Picture 관련 변수들
    ByteArrayOutputStream byteArrayOutputStream;
    byte[] buffer;
    int bytesRead;
    InputStream inputStream;
    OutputStream outputStream;
    private boolean bConnected = false;
    // 날짜 관련 변수들
    SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss");
    long now;
    Date mDate;
    String currentTime;

    public enum MessageType {
        SIMSOCK_CONNECTED(0), SIMSOCK_DATA(1), SIMSOCK_DISCONNECTED(2);
        private int value;
        private MessageType(int value) {
            value = value;
        }
        public int getValue() {
            return value;
        }
    }

    // Constructor
    public ClientSocket(String addr, int port, Handler handler, Context context){
        this.addr = addr;
        this.port = port;
        this.handler = handler;
    }

    private boolean connect(String addr, int port) {

        try{
            InetSocketAddress socketAddress = new InetSocketAddress(addr, port);
            socket = new Socket();
            socket.connect(socketAddress, 5);
        }catch(IOException e){
            System.out.println(e);
            e.printStackTrace();
            Log.d("SocketLog", e.toString());
            return false;
        }
        return true;
    }

    private void makeMessage(MessageType mType, Object obj) {
        Message msg = Message.obtain();
        msg.what = mType.ordinal();
        msg.obj = obj;
        handler.sendMessage(msg);
    }

    synchronized public boolean isConnected(){
        return bConnected;
    }

    @Override
    public void run(){

        // connect
        if(!connect(addr, port)) {
            Log.d("SocketLog", "Connected Fail !!");
            Log.d("SocketLog", "address" + addr + " " + port);
            return;
        }
        if(socket == null) return;

        // buffer receiver & sender
        try{
            inputStream = socket.getInputStream();
            outputStream = socket.getOutputStream() ;
        }catch (IOException e){
            System.out.println(e);
            e.printStackTrace();
        }

        bConnected = true;

        // send socket connection message to Handler
        makeMessage(MessageType.SIMSOCK_CONNECTED, "");
        Log.d("SocketLog", "socket_thread start !!");


        ObjectOutputStream outputStream = null;
        try {
            outputStream = new ObjectOutputStream(socket.getOutputStream());
            outputStream.writeObject("hello");
            outputStream.flush();
        } catch (IOException e) {
            e.printStackTrace();
        }



        while(!Thread.interrupted()){

            // 현재 시간
            now = System.currentTimeMillis();
            mDate = new Date(now);
            currentTime = simpleDateFormat.format(mDate);
            makeMessage(MessageType.SIMSOCK_DATA, "");
            Log.d("SocketLog", Integer.toString(bytesRead));
            makeMessage(MessageType.SIMSOCK_DISCONNECTED, "");
            Log.d("SocketLog", "socket_thread terminated !!");

        }

        try {
            byteArrayOutputStream.close();
            inputStream.close();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        bConnected = false;

    }

}