package org.newsapp.dto.task;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import org.newsapp.domain.Task;

import java.time.LocalDateTime;

@NoArgsConstructor
@RequiredArgsConstructor
@Getter
@Setter
public class TaskResponse {

    private String name;
    private String keyword;
    private String schedule;
    private LocalDateTime createdDate;
    private LocalDateTime modifiedDate;

    public TaskResponse(Task task) {
        this.name = task.getName();
        this.keyword = task.getKeyword();
        this.schedule = task.getSchedule();
        this.createdDate = task.getCreatedDate();
        this.modifiedDate = task.getModifiedDate();
    }
}
