package org.newsapp.dto.task;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import org.newsapp.domain.task.Task;

@NoArgsConstructor
@AllArgsConstructor
@Getter
public class TaskRequestDTO {
    private String name;
    private String keyword;
    private String schedule;
    private Integer days;

    public Task toEntity() {
        return Task.builder()
                .name(name)
                .keyword(keyword)
                .schedule(schedule)
                .days(days)
                .build();
    }
}
