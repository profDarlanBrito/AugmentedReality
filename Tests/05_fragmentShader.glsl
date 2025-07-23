#version 330 core

out vec4 fragColor;
void main(){
    float value = gl_FragCoord.y / 500.0;
    fragColor = vec4(value,0.0,0.0,1.0);
}