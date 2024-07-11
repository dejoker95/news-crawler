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
    private Integer days;
    private ZonedDateTime createdAt;
    private ZonedDateTime modifiedAt;

    public TaskResponseDTO(Task task) {
        this.id = task.getId();
        this.name = task.getName();
        this.keyword = task.getKeyword();
        this.schedule = task.getSchedule();
        this.days = task.getDays();
        this.createdAt = task.getCreatedAt();
        this.modifiedAt = task.getModifiedAt();
    }
}
