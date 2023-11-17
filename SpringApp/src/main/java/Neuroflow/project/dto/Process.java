package Neuroflow.project.dto;

import lombok.Data;

@Data
public class Process {

    private byte[] image;

    public Process(byte[] image) {
        this.image = image;
    }

}
