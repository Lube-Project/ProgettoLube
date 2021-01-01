import * as React from 'react';
interface IProps {
    year: number;
    month: number;
    value: number;
    onChange: Function;
    id?: string;
    name?: string;
    defaultValue?: string;
    endYearGiven?: boolean;
    required?: boolean;
    disabled?: boolean;
    classes?: string;
    optionClasses?: string;
}
interface IState {
}
export declare class DayPicker extends React.Component<IProps, IState> {
    renderDayOptions: () => JSX.Element[];
    handleSelectionChange: (e: any) => any;
    render: () => JSX.Element;
}
export {};
