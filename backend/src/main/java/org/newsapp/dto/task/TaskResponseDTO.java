package org.newsapp.dto.task;

import lombok.*;
import org.newsapp.domain.task.Task;

import java.time.ZonedDateTime;

@NoArgsConstructor
@AllArgsConstructor
@Getter
public class TaskResponseDTO {

    private Long id;
    private String name;
    private String keyword;
    private String schedule;
    private Long hours;
    private ZonedDateTime createdAt;
    private ZonedDateTime modifiedAt;

    public TaskResponseDTO(Task task) {
        this.id = task.getId();
        this.name = task.getName();
        this.keyword = task.getKeyword();
        this.schedule = task.getSchedule();
        this.hours = task.getHours();
        this.createdAt = task.getCreatedAt();
        this.modifiedAt = task.getModifiedAt();
    }
}
